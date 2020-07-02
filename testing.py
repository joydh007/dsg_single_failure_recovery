# from datetime import datetime

# date_time_str = '2020-06-27 18:55:19.015100'
# current_time = datetime.now()



# print(current_time)
# print(date_time_str)
# # print ("The date is", date_time_obj)
# date_time_obj = datetime.strptime(date_time_str, '%y-%m-%d %H:%M:%S.%f\n')
# diff = current_time - date_time_obj
# print ("The type of the date is now",  date_time_obj)
# print(diff)

# import time
# import datetime
# from datetime import datetime, date

# test = datetime.min.time()
# print(test)
# date_time_str = '20:01:08.336065'
# current_time = datetime.now().time()
# print(current_time)

# date_time_obj = datetime.strptime(date_time_str, '%H:%M:%S.%f').time()
# diff = datetime.combine(date.today(), current_time) - datetime.combine(date.today(), date_time_obj)

# print ('The type of the date is now', date_time_obj)
# # diff = (current_time - date_time_obj)
# print(diff)

import in_place

with in_place.InPlace('new.txt')as file:
    for line in file:
        # if line == "loves"
        line = line.replace('already written', '\n')
        file.write(line)