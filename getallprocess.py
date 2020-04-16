import psutil
# Iterate over all running process
# for proc in psutil.process_iter():
#     try:
#         processName = proc.name()
#         processID = proc.pid
#         print(processName , ' ::: ', processID)
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass

for proc in psutil.process_iter():
    if proc.name() == "python.exe":
        print(proc.pid)
        proc.kill()


# except KeyboardInterrupt:
#         print "Caught KeyboardInterrupt, terminating workers"
#         pool.terminate()
#         pool.join()