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
import numpy as np
import statistics
from fractions import Fraction as fr
import itertools
import math
from typing import Any

# location = 'F:/fib_data_archive/2014/'  # /mnt/fib_archive/2013
#
# for root, dirs, files in os.walk(location):
# 	for file in files:
# 		if file.split('.')[-1] == 'xz':
# 			print(str(file))

# all = ['2013/', '2014/', '2016/', '2017/', '2018/', '2019/']
# location = 'F:/fib_data_archive/'  # /mnt/fib_archive/     F:/fib_data_archive/
# unzipLocation = 'F:/fib_data_archive/2013/2013-11-12_backup/2013-11-12.tar.xz'
# f = '/mnt/fib_archive/2014_extract/hbone_vh2_2014_05_18_00_32_46.txt'

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

# lst= []
# for o in range(10,20):
# 	b=[]
# 	for i in range(6):
# 		b.append(str(o)+str(i))
# 	lst.append(b)
# print(lst)
#

out_location = 'D:/x/teszt_compare/'
rle_location = 'D:/x/rle/'
two32 = 2 ** 32
today = datetime.date.today().strftime("%y-%m-%d")

a_files = []
b_files = []
for root, dirs, files in os.walk(rle_location):
	for file in files:
		if "bme" in file or "szeged" in file or "vh1" in file or "vh2" in file:
			a_files.append(file)
		else:
			b_files.append(file)
files = []
files.append(a_files)
files.append(b_files)
'''
Összes kombináció megadása
'''
for e in itertools.product(*files):
	a = e[0]
	b = e[1]
	a_lst = []
	b_lst = []
	a_nh = []
	b_nh = []
	name_a = a.split("_")[0]
	name_b = b.split("_")[0]
	out_name = name_a + "_" + name_b + "_" + today + ".txt"
	print(name_a, name_b)
