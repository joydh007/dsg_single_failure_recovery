import sys
import os
import shutil

print(os.listdir())
Name_of_node = sys.argv[1]
shutil.move(Name_of_node, 'copy')
print(os.listdir())
