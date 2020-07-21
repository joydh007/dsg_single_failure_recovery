import os
import signal
import sys
import shutil
import datetime
import in_place


kill_node = sys.argv[1]
print("Node to kill -> ",kill_node)
with open('process_ids.txt') as file:
    for line in file:
        if line.strip() != "":
            stripped_line = line.strip()
            print(stripped_line)
            line_info_list = stripped_line.split(':')
            node_id = line_info_list[0]
            process_id = line_info_list[1]
            pid = int(process_id)
            if node_id == kill_node:
                kill_id = pid
                print(f'--------{kill_node} Node will be killed ---------')
                os.kill(pid, signal.SIGTERM)
        else:
            pass

shutil.move(kill_node, 'copy')
detection_time_start = datetime.datetime.now().time()
store_time = open('kill_log.txt', 'a+')
store_time.write(f'{kill_node}kill_time={detection_time_start}')
store_time.write("\n")
store_time.close()

with in_place.InPlace('process_ids.txt')as file:
    for line in file:
        line = line.replace(f'{kill_node}:{kill_id}', '')
        file.write(line)
