import os
import sys
import asyncio
import string
import random
import time
import fnmatch


class random_creation():
    def __init__(self, path,):
        self.path = path


    
    def string_generator(self, size,):
        chars = string.ascii_uppercase + string.ascii_lowercase
        return ''.join(random.choice(chars) for _ in range(size))
    # data = string_generator(10)

    def send(self, name,):
        self.name = name
        f = open(f'{path}/{name}.txt', 'a+')
        f.write(data +"\n")
    # await asyncio.sleep(5)


if __name__ == '__main__':
    list = sys.argv[2:]
    path = os.path.realpath(sys.argv[1])
    print(list)
    h = random_creation(path)
    # data = h.string_generator(10)
    for i in list:
        h.send(i)
        # f = open(f'{path}/{i}.txt', 'a+')
        # f.write(data +"\n")

    # async def send():
    #     while True:
    #         for i in list:
    #             f = open(f'{path}/{i}.txt', 'a+')
    #             f.write(data +"\n")
    #             await asyncio.sleep(5)
    #         # time.sleep(5)


    # for file_name in os.listdir('some_directory/'):
    #     if fnmatch.fnmatch(file_name, '*.txt'):
    #         print(file_name)