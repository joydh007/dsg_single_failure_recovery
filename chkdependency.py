import asyncio
import time
import sys
import os

from util import int2bytes, bytes2int, run
from radio import Radio
from pubsub import Pub, Sub
from freeport import get_free_tcp_port


class ChkDependency():
    def __init__(self, path, lst, port):
        self.path = path
        self.lst = lst
        self.port = port
        self.radio = radio
        self.pub = pub
        self.sub = sub
    
    def makeDir(self):
        try:
            os.mkdir(self.path)
        except OSError:
            print ("Creation of the directory %s failed" % path)
        else:
            print ("Successfully created the directory %s" % path)

        for vertex in (self.lst):
            f = open(f'{path}/{vertex}.txt', 'a+')
            f.close() 


    async def radiostart(self):
        while True:
            await asyncio.sleep(2)
            self.radio.start()
        print("Radio is initialized")
        await asyncio.sleep(2)
        
    async def send(self, message):
        await asyncio.sleep(2)
        self.radio.send()
        return

    async def pubstart(self, topic, message):
        await asyncio.sleep(2)
        print("pub is initialized")
        pub.socket.send_multipart([
            bytes(topic, 'utf8'),
            bytes(message, 'utf8')
        ])
        

    async def heartbeat(self):
        
        print("heartbeat started")
        await asyncio.sleep(2)
        
        

    async def idmatch(self):
        
        await asyncio.sleep(2)
        print("checking for matches in neigh list")
        
        

    async def substart(self, topic, listener):
        await asyncio.sleep(2)
        print("match found")
        await asyncio.sleep(2)
        sub.socket.setsockopt(zmq.SUBSCRIBE, bytes(topic, 'utf8'))
        string = await sub.socket.recv_multipart()
        listener(string)
        print("receiving...")
        print("subscribing.....")

        

    async def start(self):
        self.makeDir()
        while True:
            await asyncio.wait([
                Chkdependency.radiostart(),
                Chkdependency.pubstart('1001100', 'hello'),
                Chkdependency.heartbeat(),
                Chkdependency.idmatch(),
                Chkdependency.substart('1001100', print),
            ])    
        

    

if __name__ == '__main__':
    lis = sys.argv[2:]
    o_path = os.path.abspath(os.path.realpath(sys.argv[1]))
    path = (f'{o_path}/{lis[0]}')
    port = get_free_tcp_port()
    # radio = Radio(port, lambda m, a, p: print(
    #         f"{a}:{p} → {bytes2int(m):08b}"))
    # pub = Pub(port)
    # sub = Sub(port)
    Chkdependency = ChkDependency(path, lis, port)
    # Chkdependency.radio = Radio(port, lambda m, a, p: print(
    #         f"{a}:{p} → {bytes2int(m):08b}"))
    # Chkdependency.pub = Pub(port)
    # Chkdependency.sub = Sub(port)
    t0 = time.time()
    # async def start():
    #     while True:
    #         await asyncio.wait([
    #             a.radio(),
    #             a.pub(),
    #             a.heartbeat(),
    #             a.idmatch(),
    #             a.sub(),
    #         ])    
    

    # loop = asyncio.get_event_loop()
    # loop.run_until_complete(Chkdependency.start())
    # loop.close()

    try:
        run(
            Chkdependency.start(),
          )
    except KeyboardInterrupt:
        print("Exiting...")
        t1 = time.time()
        print("Took time : ",(t1-t0))
        exit()