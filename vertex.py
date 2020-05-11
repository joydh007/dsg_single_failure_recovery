import sys
import os
import asyncio
import string
import random
import time
import linecache
import operator

from threading import Condition, Thread
from pubsub import Pub, Sub
from radio import Radio
from util import int2bytes, bytes2int, run
from free_port import get_free_tcp_port, get_free_tcp_address
from pushpull import Push, Pull

RADIO_PORT = 55555
MSG_TOPIC = '10001'
STR_RANGE = 10
PP_PORT = get_free_tcp_port()
total_broadcast_no = 5
LINE = 1
COUNTER = 0


class Vertex():
    def __init__(self, path, neighbourhood):
        self.path = path
        self.neighbourhood = neighbourhood
        self.port = get_free_tcp_port()
        self.pp_port = get_free_tcp_port()
        self.radio_started = asyncio.Event()
        self.pub_started = asyncio.Event()
        self.heart_beat_started = asyncio.Event()
        self.subbed_neighbors = {}
        self.pushed_neighbours = {}
        self.sub_listen_task = {}
        self.getting_ready_to_write = asyncio.Event()
        self.has_finished_writing = asyncio.Event()
        self.bands = []
        self.no_of_sender = []
        self.tic = time.time()
        self.toc = time.time()
        self.redis = {}    
        # self.lock = asyncio.Lock()

    def makeDir(self):
        try:
            os.mkdir(self.path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s" % path)

        for vertex in (self.neighbourhood):
            f = open(f'{path}/{vertex}.txt', 'a+')
            f.close() 

    async def init_radio(self):
        self.radio = Radio(RADIO_PORT, self.neighbourhood_watch)
        self.radio_started.set()
        print(f"1 Radio Started {self.port}, self id: {self.neighbourhood[0]}, neighbour list: {self.neighbourhood[1:]}")
        await self.radio.start()

    async def init_pub(self):
        self.pub = Pub(self.port)
        self.pub_started.set()
        print('2 Pub Started')
        while True:
            if len(self.neighbourhood[1:]) is len(self.subbed_neighbors.keys()) and self.neighbourhood[1:]:
                chars = string.ascii_uppercase + string.ascii_lowercase
                msg = ''.join(random.choice(chars) for _ in range(STR_RANGE))
                print(f'Sending: {msg}' )
                self.pub.send(MSG_TOPIC, msg)
            await asyncio.sleep(15)

    async def init_heart_beat(self):
        await self.radio_started.wait()
        await self.pub_started.wait()
        self.heart_beat_started.set()
        while True:
            self.tic = time.time()
            # print(f'\n heartbeat timer {self.tic} \n')
            if not self.neighbourhood[1:]:       
                self.recovery_pull = Pull(PP_PORT)
                asyncio.create_task(self.recovery_pull.listen(self.gather_msg))
                for broadcasting_no in range(total_broadcast_no):
                    msg = f'lost,{self.port},{PP_PORT},{self.neighbourhood[0]}'
                    self.radio.send(bytes(msg, 'utf-8'))
                    print(f"LOST msg broadcasting: {msg}")
                    await asyncio.sleep(5)
                self.recovery_pull.pull_cancel()
            else:
                msg = f'ready,{self.port},{self.pp_port},{self.neighbourhood[0]}'
                self.radio.send(bytes(msg, 'utf-8'))
                print(f"Heart beat broadcasting: {self.port}, {self.neighbourhood[0]}")
                await asyncio.sleep(5)

    def neighbourhood_watch(self, msg, addr, port):
        if self.neighbourhood[1:]:
            str_msg = str(msg, 'utf-8')
            msg_list = str_msg.split(',')
            vertex_msg = msg_list[0]
            vertex_port = msg_list[1]
            vertex_pp_port = msg_list[2]
            vertex_id = msg_list[3]
            self.toc = time.time()
            # print(f'\n neighbour timer {self.toc} \n')
            global COUNTER
            return_time = (self.toc - self.tic)
            if return_time < 10:
                self.redis[vertex_id] = COUNTER + 1
            else:
                self.redis[vertex_id] = COUNTER 
            COUNTER = COUNTER + 1
            # print(self.redis)
            print(f'Received Heartbeat from {vertex_id} : {vertex_port} → {msg} : {vertex_msg}')
            if vertex_msg == 'ready' and vertex_id in self.neighbourhood [1:] and vertex_id not in self.subbed_neighbors:
                print(f'Match found from ready msg {vertex_id}')
                sub = Sub(vertex_port)
                self.subbed_neighbors[vertex_id] = sub
                # print(self.subbed_neighbors)
                task = asyncio.create_task(sub.listen(MSG_TOPIC, self.post_msg))
                self.sub_listen_task[vertex_id] = task
                push = Push(vertex_pp_port)
                print(self.pushed_neighbours)
                self.pushed_neighbours[vertex_id] = push
                print(self.pushed_neighbours)
                print(f'From neighbourhood watch msg = ready {self.subbed_neighbors}{self.pushed_neighbours}')
            elif vertex_msg == 'lost' and vertex_id in self.neighbourhood [1:] and vertex_id in self.subbed_neighbors:
                task_instance = self.sub_listen_task[vertex_id]
                task_instance.cancel()
                instance = self.subbed_neighbors[vertex_id]
                instance.sub_cancel()
                del self.subbed_neighbors[vertex_id]
                pInstance = self.pushed_neighbours[vertex_id]
                pInstance.push_cancel()
                del self.pushed_neighbours[vertex_id]
                self.recovery_push = Push(vertex_pp_port)
                file = open(f'{self.path}/{vertex_id}.txt', 'r')
                for line_no, line in enumerate(file, 1):
                    self.recovery_push.send(f'{self.neighbourhood[0]}:{line}')
                print(f'From neighbourhood watch msg = lost {self.subbed_neighbors}{self.pushed_neighbours}')
            self.Someone_failed()
    
    def Someone_failed(self):
        minval = min(self.redis.values())
        for value in self.redis.values():
            if value - minval >= 10:
                Keys = [x for x in self.redis if self.redis[x] == minval]
                print("failed node is \n ",Keys)
            else:
                continue
    def post_msg(self, payload):
        msg = str(payload[1], 'utf-8')
        print(f'Received msg: {msg}')
        f = open(f'{self.path}/{self.neighbourhood[0]}.txt', 'a+')
        f.write(f'{msg}\n')
        f.close()

    async def partial_replication(self):
        await self.heart_beat_started.wait()
        print('Partial Replication Started')
        self.pull = Pull(self.pp_port)
        asyncio.create_task(self.pull.listen(self.replicate_msg))
        line_no = 1
        while True:
            if self.neighbourhood[1:] and len(self.neighbourhood[1:]) == len(self.pushed_neighbours.keys()) and len(self.neighbourhood[1:]) == len(self.subbed_neighbors.keys()):
            # if self.neighbourhood[1:]:
                # file = open(f'{self.path}/{self.neighbourhood[0]}.txt', 'r')
                file = f'{self.path}/{self.neighbourhood[0]}.txt'
                while file is None:
                    await asyncio.sleep(5)
                line = linecache.getline(file, line_no)
                while not line:
                    await asyncio.sleep(5)
                    linecache.clearcache()
                    line = linecache.getline(file, line_no)
                    print(f'New line: {line}')
                round_robin_id = self.neighbourhood[line_no % (len(self.neighbourhood) - 1) + 1]
                if round_robin_id in self.pushed_neighbours.keys():
                    self.pushed_neighbours[round_robin_id].send(f'{self.neighbourhood[0]},{line_no},{line}')
                    print(f'Vertex No: {round_robin_id}, data: {line}')
                line_no = line_no + 1
                # for line_no, line in enumerate(file, 1):
                #     # if self.neighbourhood[1:] and len(self.neighbourhood[1:]) == len(self.pushed_neighbours.keys()) and len(self.neighbourhood[1:]) == len(self.subbed_neighbors.keys()):
                #         # round_robin_id = self.neighbourhood[line_no % (len(self.neighbourhood) - 1) + 1]
                #         # print(f'Vertex No: {round_robin_id}, data: {line}')
                #         # if round_robin_id in self.pushed_neighbours.keys():
                #         #     self.pushed_neighbours[round_robin_id].send(f'{self.neighbourhood[0]},{line_no},{line}')
                #         #     print(f'Vertex No: {round_robin_id}, data: {line}')
                #     round_robin_id = self.neighbourhood[line_no % (len(self.neighbourhood) - 1) + 1]
                #     if round_robin_id in self.pushed_neighbours.keys():
                #         self.pushed_neighbours[round_robin_id].send(f'{self.neighbourhood[0]},{line_no},{line}')
                #         print(f'Vertex No: {round_robin_id}, data: {line}')
                    # await asyncio.sleep(5)
                # await asyncio.sleep(5)
                # file.close()
            await asyncio.sleep(5)
        
    def replicate_msg(self, rec_payload):
        message = str(rec_payload, 'utf-8')
        message_list = message.split(',')
        rec_vertex_id = message_list[0]
        line_no = message_list[1]
        line_data = message_list[2]
        file = open(f'{self.path}/{rec_vertex_id}.txt', 'a+')
        file.write(f'{line_no}:{line_data}')
        file.close()

    def gather_msg(self, message):
        message = str(message, 'utf-8')
        message_list = message.split(':')
        rec_vertex_id = message_list[0]
        line_no = int(message_list[1])
        line_data = message_list[2]
        self.no_of_sender.append([rec_vertex_id])
        print(self.no_of_sender)
        global LINE
        # try:
        if line_no != LINE:
            self.bands.append(tuple([line_no, line_data]))
        self.bands.sort(key = operator.itemgetter(0))
        print(self.bands)
        if line_no == LINE:
            with open(f'{self.path}/{self.neighbourhood[0]}.txt', 'a+') as fileout:
                for band in self.bands:
                    fileout.write(f'{band[0]}:{band[1]}')
                self.bands.clear()
                fileout.write(f'{line_no}:{line_data}')
        if self.no_of_sender.count(self.no_of_sender[0]) == 2:
            # unique_values = set(self.no_of_sender)
            # unique_count = len(unique_values)
            with open(f'{self.path}/{self.neighbourhood[0]}.txt', 'a+') as fileout:
                for band in self.bands:
                    fileout.write(f'{band[0]}:{band[1]}')
                self.bands.clear()
                self.no_of_sender.clear()
        LINE = LINE + 1
            # print(self.bands)
        # except:
        #     with open(f'{self.path}/{self.neighbourhood[0]}.txt', 'a+') as fileout:
        #         for band in self.bands:
        #             fileout.write(f'{band[0]}:{band[1]}')
        #         self.bands.clear()
        if rec_vertex_id not in self.neighbourhood[1:]:
            self.neighbourhood.append(rec_vertex_id)
        # print(self.neighbourhood)

    # def gather_msg(self, message):
    #     message = str(message, 'utf-8')
    #     message_list = message.split(':')
    #     rec_vertex_id = message_list[0]
    #     line_no = message_list[1]
    #     line_data = message_list[2]
    #     file = open(f'{self.path}/{self.neighbourhood[0]}.txt', 'a+')
    #     file.write(f'{message}')
    #     file.close()
    #     if rec_vertex_id not in self.neighbourhood[1:]:
    #         self.neighbourhood.append(rec_vertex_id)
    #     print(self.neighbourhood)

    async def start(self):
        self.makeDir()
        await asyncio.gather(
            self.init_radio(),
            self.init_pub(),
            self.init_heart_beat(),
            self.partial_replication(),
        )

    
if __name__ == '__main__':
    lis = sys.argv[2:]
    o_path = os.path.abspath(os.path.realpath(sys.argv[1]))
    path = (f'{o_path}/{lis[0]}')
    vertex = Vertex(path, lis)

    try:
        run(
            vertex.start()
        )
    except KeyboardInterrupt:
        print("Exiting...")
        exit()