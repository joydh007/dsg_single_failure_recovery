# import psutil
 
# for proc in psutil.process_iter():
#     try:
#         # Get process name & pid from process object.
#         processName = proc.name()
#         processID = proc.pid
#         print(processName , ' ::: ', processID)
#     except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
#         pass

# for proc in psutil.process_iter():
#     if proc.name() == "powershell.exe":
#         proc.kill()

import psutil
import os

my_pid = os.getpid()

for proc in psutil.process_iter():
    try:
        # Get process name & pid from process object.
        processName = proc.name()
        processID = proc.pid

        if proc.pid == my_pid:
            print("I am not suicidal")
            continue

        if processName.startswith("controller"): # adapt this line to your needs
            print(f"I will kill {processName}[{processID}] : {''.join(proc.cmdline())})")
            proc.kill()
    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
        print(e)