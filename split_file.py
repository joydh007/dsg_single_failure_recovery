import os
import sys

def split_file(path, neighbourhood):
    # splitLen = 4
    f = open(f'{path}\{neighbourhood[0]}.txt','r').read().split('\n')
    length = len(neighbourhood) - 1
    print(length)
    linetotal = len(f)
    print(linetotal)
    splitLen = int(linetotal / length)
    print(splitLen)
    i = 1
    for lines in range(0, len(f), splitLen):
        slpitdata = f[lines: lines + splitLen]
        output = open(f'{path}/{neighbourhood[i]}.txt', 'w')
        output.write('\n'.join(slpitdata))
        output.close()
        i += 1
        print("succesfully splited")

if __name__=="__main__":
    lis = sys.argv[2:]
    o_path = os.path.abspath(os.path.realpath(sys.argv[1]))
    path = (f'{o_path}\{lis[0]}')
    split_file(path, lis)