import sys
import os
import re

bands = list()
filename = "check.txt"
filein = open(filename, "r")
for num, line in enumerate(filein):
    number = [int(word) for word in line.split() if word.isdigit()]
    n = number[0]
    print(n)
    char = "".join(re.split("[^a-zA-Z]*", line))
    print(char)
    bands.append(tuple([n, char]))
bands.sort()
print(bands)
filein.close()
with open(filename, "w") as fileout:
    for band in bands:
        fileout.write(f'{band[0]}:{band[1]}'+'\n')
fileout.close()


# bands = list()
# filename = "check.txt"
# filein = open(filename, "r")
# for num, line in enumerate(filein):
#     number = [int(word) for word in line.split() if word.isdigit()]
#     n = number[0]
#     print(n)
#     char = "".join(re.split("[^a-zA-Z]*", line))
#     print(char)
#     bands.append(tuple([n, char]))

# bands.sort()
# print(bands)

# filename = "try.txt"
# with open(filename, "w") as fileout:
#     for band in bands:
#         fileout.write(f'{band[0]}:{band[1]}'+'\n')

