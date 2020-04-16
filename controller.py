import sys
import os
import signal
import csv
import subprocess
from subprocess import Popen, CREATE_NEW_CONSOLE

file_path = os.path.realpath(sys.argv[1])

reader = csv.reader(open(file_path), delimiter=',', quotechar=' ')
# pid = os.getpid()
# with open('pid.csv','a',newline='\n') as csvfile:
#     wr = csv.writer(csvfile)
#     wr.writerow(['controller', pid])

dictionary = {}

for row in reader:
    x = row[0]
    y = row[1]
    dictionary.setdefault(x, []).append(y)
    dictionary.setdefault(y, []).append(x)

for vertex in dictionary:
    neigh = ' '.join(dictionary[vertex])
    pid = os.getpid()
    print(pid)
    try:
        # subprocess.Popen(f'python ./vertex.py ./ {vertex} {neigh}', creationflags=CREATE_NEW_CONSOLE)
        subprocess.Popen(f'python ./vertexn.py ./ {vertex} {neigh}', shell=True)
    except KeyboardInterrupt:
        print("Exiting...")
        pid = os.getpid()
        print(pid)
        os.kill(os.getpid(), signal.SIGTERM)
        exit()
    # except KeyboardInterrupt:
    #     print("Exiting...")
    #     # subprocess.call(f'python ./kill.py ./ {pid}', shell=True)
    #     exit()
# # wait for exit or timeout
# if timeout:
#   

    # subprocess.Popen(f'python ./vertex.py ./ {vertex} {neigh}', creationflags=CREATE_NEW_CONSOLE)
    # subprocess.call('python pi.txt', shell=True)
    # Run: D:\Educational\dsg_single_faliure_recovery\src> python .\controller.py ..\data\facebook_data.csv