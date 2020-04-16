
# def killsubprocesses(parent_pid):
#     '''kill parent and all subprocess using COM/WMI and the win32api'''
    
#     log = logging.getLogger('killprocesses')
    
#     try:
#         import comtypes.client
#     except ImportError:
#         log.debug("comtypes not present, not killing subprocesses")
#         return
#     if processes_to_kill:
#         log.info('Process pid %i spawned %i subprocesses, terminating them...' % 
#             (parent_pid, len(processes_to_kill)))
#     else:
#         log.debug('Process pid %i had no subprocesses.' % parent_pid)

import os
import signal
import pandas as pd
import psutil
# pid = pd.read_csv('pid.csv', names = ['prog','pid'])
    # def killsubprocesses(pid):
my_pid = 34024
print(my_pid)
try:
    for proc in psutil.process_iter():
        proc.kill()
    # os.kill(pid['pid'][x],signal.SIGTERM)
except:
    pass

# p = subprocess.POpen(....)
# # wait for exit or timeout
# if timeout:
#   subprocess.call(['taskkill', '/F', '/T', '/PID', str(p.pid)])

# If you don't want to run another program, there's the long way around, by using comtypes and ctypes to access the WMI and Win32 API functions. I wrote this before I found out about the above, but it was easy to port C++ samples to this, and I already had comtypes in our system. Maybe it's useful for someone...

# def killsubprocesses(parent_pid):
#     '''kill parent and all subprocess using COM/WMI and the win32api'''
    
#     log = logging.getLogger('killprocesses')
    
#     try:
#         import comtypes.client
#     except ImportError:
#         log.debug("comtypes not present, not killing subprocesses")
#         return
    
#     logging.getLogger('comtypes').setLevel(logging.INFO)
    
#     log.debug('Querying process tree...')

#     # get pid and subprocess pids for all alive processes
#     WMI = comtypes.client.CoGetObject('winmgmts:')
#     processes = WMI.InstancesOf('Win32_Process')
#     subprocess_pids = {} # parent pid -> list of child pids
    
#     for process in processes:
#         pid = process.Properties_('ProcessID').Value
#         parent = process.Properties_('ParentProcessId').Value
#         log.trace("process %i's parent is: %s" % (pid, parent))
#         subprocess_pids.setdefault(parent, []).append(pid)
#         subprocess_pids.setdefault(pid, [])
      
#     # find which we need to kill
#     log.debug('Determining subprocesses for pid %i...' % parent_pid)

#     processes_to_kill = []
#     parent_processes = [parent_pid]
#     while parent_processes:
#         current_pid = parent_processes.pop()
#         subps = subprocess_pids[current_pid]
#         log.debug("process %i children are: %s" % (current_pid, subps))
#         parent_processes.extend(subps)
#         processes_to_kill.extend(subps)

#     # kill the subprocess tree
#     if processes_to_kill:
#         log.info('Process pid %i spawned %i subprocesses, terminating them...' % 
#             (parent_pid, len(processes_to_kill)))
#     else:
#         log.debug('Process pid %i had no subprocesses.' % parent_pid)

#     import ctypes
#     kernel32 = ctypes.windll.kernel32
#     for pid in processes_to_kill:
#         hProcess = kernel32.OpenProcess(PROCESS_TERMINATE, FALSE, pid);
#         if not hProcess:
#             _log.warning('Unable to open process pid %i for termination' % pid)
#         else:
#             _log.debug('Terminating pid %i' % pid)                        
#             kernel32.TerminateProcess(hProcess, 3)
#             kernel32.CloseHandle(hProcess)

# This code could of course be improved by not walking all processes,