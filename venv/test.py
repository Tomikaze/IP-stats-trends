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

filepath = "C:/fib data archive/extract/hbone_bme_2019_06_01_00_10_07.txt"
location = 'C:/fib data archive'
ouf = 'C:/teszt/act.txt'
workFiles = []

storeList = []

vh1 = "^hbone_vh1"
vh2 = "^hbone_vh2"
bme = "^hbone_bme"
szeged = "^hbone_szeged"


class Ip:
	time_stamp = ''
	address = 0
	prefix = 0
	ip = 0
	msp = 0
	bin = ''

	def __init__(self, address, prefix, ip):
		self.address = address
		self.prefix = prefix
		self.ip = ip

	def tostring(self):
		return str(self.bin) + '\t' + str(self.address) + '\t' + str(self.ip) + '\t' + str(self.prefix) + '\t' + str(
			self.msp)

	def write_pre_bin(self):
		return str(self.bin[0:int(self.prefix)])


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

	storeList.clear()
	with open(filepath) as fp:
		line = fp.readline()
		# default gateway kihagyása
		if line[8] == '0':
			line = fp.readline()
		cnt = 1
		while line:
			# print("Line {}: {}".format(cnt, line.strip()))
			tmp = line.split("\t")
			tmp2 = tmp[0].split("/")

			# diagram 3 hoz prefix ek számolása

			p = Ip(tmp2[0], tmp2[1], tmp[1].strip())
			prefix = tmp2[0].split(".")
			for i in prefix:
				p.bin += bin(int(i))[2:].zfill(8)

			if cnt == 1:
				storeList.append(p)
				cnt += 1

			if (cnt > 1 and not (storeList[storeList.__len__() - 1].address == p.address and storeList[
				storeList.__len__() - 1].prefix == p.prefix)):
				storeList.append(p)
				# print(storeList[cnt-1].address)
				cnt += 1
			line = fp.readline()

with open(ouf, 'w+') as f:
	for i in storeList:
		f.write(i.write_pre_bin() + '\n')
	f.close()
