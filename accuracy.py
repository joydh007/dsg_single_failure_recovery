import itertools
import os
import sys
import shutil

Name_of_node = sys.argv[1]
Compare_with = "copy" 
count = 0
total = 0

files = os.listdir(Name_of_node)
print(files)
for f in files:
    print(f)
    with open(f'{Compare_with}/{f}') as f1, open(f'{Name_of_node}/{f}') as f2:
        for lineno, (line1, line2) in enumerate(itertools.zip_longest(f1, f2), 1):
            total = total + 1
            if line1 != line2 and line1 != None:
                print(f'mismatch of file {f} in line no:', lineno)
                print(f'{line1}  {line2}')
                count = count + 1
print("total lines & mismatched lines :", total, count)
accuracy = ((total - count)/total)*100
print('accuracy rate-----> ', round(accuracy,4))
record = open('Output.txt', 'a+')
record.write(f'Accuracy Rate of recovery = {accuracy}')
record.write('------------------------------------------------------------\n')
record.close()
shutil.rmtree('copy')
