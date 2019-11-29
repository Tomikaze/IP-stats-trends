import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
import datetime
from datetime import date
from prefixtree import TrieNode, add, sum_level, count_first_letter
from multiprocessing import Pool, Lock
import time
import copy
import random


# location = 'F:/fib_data_archive/2014/'  # /mnt/fib_archive/2013
#
# for root, dirs, files in os.walk(location):
# 	for file in files:
# 		if file.split('.')[-1] == 'xz':
# 			print(str(file))

all = ['2013/', '2014/', '2016/', '2017/', '2018/', '2019/']
location = 'F:/fib_data_archive/'  # /mnt/fib_archive/     F:/fib_data_archive/
unzipLocation = 'F:/fib_data_archive/2013/2013-11-12_backup/2013-11-12.tar.xz'
f = '/mnt/fib_archive/2014_extract/hbone_vh2_2014_05_18_00_32_46.txt'

# for year in all:
# 	for root, dirs, files in os.walk(location + year):
# 		for file in files:
# 			if file.split('.')[-1] == 'xz':
# 				print(root + '/' + file)
#
# print(str(unzipLocation.rsplit('/',2)[0]))
#
# save_loc = f.rsplit('_', 8)[0]
# save_name = f.rsplit('_')[-7]
# today = date.today().strftime("%y-%m-%d")
# print(today)
# file_name = save_loc + '_save_' + save_name + '_' + str(today) + '.txt'
# print(file_name)


start="\'pref_"
p="\' , \'pref_"
print(p)
for i in range(8,32):
    start+=str(i)+p
start+="32\'"
print(start)

for i in range(20):
    print(random.randint(15453988313675, 29421883821487))