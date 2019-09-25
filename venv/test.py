import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
from binarytree import tree, bst, heap, Node
from typing import Tuple
from multiprocessing import Process, Pool, Lock
import multiprocessing as mp
import math
import time
from datetime import date

location = 'C:/teszt/'


def calc(n):
	list = []

	proc = os.getpid()
	for i in range(0, 10):
		list.append(str(n) + str(i))
	print('{0}  by process id: {1}'.format(n, proc))
	return list


if __name__ == "__main__":
	# in_list = [1, 2, 3, 4, 5, 6, 7]
	# name = 'process.txt'
	#
	# pool = Pool(processes = os.cpu_count())
	# result = pool.map(calc, in_list)
	# with open(location + name, 'a+') as f:
	# 	for l in result:
	# 		f.write(str(l) + '\n')
	# 	f.close()

	name = 'hbone_bme_2019_06_27_00_10_09.txt'
	print(name.split('_',2)[1])
	print(date.today().strftime("%y-%m-%d"))