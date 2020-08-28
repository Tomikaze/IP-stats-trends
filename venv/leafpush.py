import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
import datetime
from datetime import date
from prefixtree import TrieNode, add, sum_level, count_first_letter, leafpush, printPreorder,maxDepth, make_LRE
from multiprocessing import Pool, Lock
import time
import copy

all = ['2013/']  # '2014/', '2015/', '2016/', '2017/', '2018/', '2019/']
location = '/mnt/rib_linx_fib_format/'  # /mnt/fib_archive/     F:/fib_data_archive/    F:\rib_linx_fib_format/     /mnt/rib_linx_fib_format/
rib_save_loc = '/mnt/'  # /mnt/   F:/

workFiles = []

storeList = []

vh1 = "^hbone_vh1"
vh2 = "^hbone_vh2"
bme = "^hbone_bme"
szeged = "^hbone_szeged"
rib = "_rib_"


class Save:
	time_stamp = ''
	msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	count = 0
	sum_msp = 0
	adv_range = 0
	per8 = 0

	def __init__(self):
		self.time_stamp = ''
		self.msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		                  0]
		self.pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		                   0]
		self.count = 0
		self.sum_msp = 0
		self.adv_range = 0
		self.per8 = 0

	def blank_sheet(self):
		self.time_stamp = ''
		self.msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		                  0]
		self.pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		                   0]
		self.count = 0
		self.sum_msp = 0
		self.adv_range = 0
		self.per8 = 0

	"""
		Fájlba írja az osztályt
	"""

	def end_game(self, f):
		save_loc = f.rsplit('_', 8)[0]
		save_name = f.rsplit('_')[-7]
		today = datetime.date.today().strftime("%y-%m-%d")
		file_name = save_loc + '_save_' + save_name + '_' + str(today) + '.txt'

		with open(file_name, 'a+') as f:
			# timestamp
			f.write("\n" + str(self.time_stamp))

			# prefix count 1. diagram
			f.write("\ttotal_count:")
			f.write("\t" + str(self.count))

			# sum more specific prefix count 2. diagram
			f.write("\tmsp_sum:")
			f.write("\t" + str(self.sum_msp))

			# prefix count 3. diagram
			f.write("\tpref_count:")
			for i in self.pref_count:
				f.write("\t" + str(i))

			# more specific prefixes 4. diagram
			f.write("\tmsp_count:")
			for i in self.msp_count:
				f.write("\t" + str(i))

			# per 8 range 5. diagram
			f.write("\tper 8:\t" + str(self.per8))

			f.close()

	def rib_end_game(self, f):
		today = datetime.date.today().strftime("%y-%m-%d")
		file_name = rib_save_loc + '_save_' + f + '_' + str(today) + '.txt'

		with open(file_name, 'a+') as f:
			# timestamp
			f.write("\n" + str(self.time_stamp))

			# prefix count 1. diagram
			f.write("\ttotal_count:")
			f.write("\t" + str(self.count))

			# sum more specific prefix count 2. diagram
			f.write("\tmsp_sum:")
			f.write("\t" + str(self.sum_msp))

			# prefix count 3. diagram
			f.write("\tpref_count:")
			for i in self.pref_count:
				f.write("\t" + str(i))

			# more specific prefixes 4. diagram
			f.write("\tmsp_count:")
			for i in self.msp_count:
				f.write("\t" + str(i))

			# per 8 range 5. diagram
			f.write("\tper 8:\t" + str(self.per8))

			f.close()

	def set_sum_msp(self):
		for i in self.msp_count:
			self.sum_msp += i

	def set_date(self, f):
		self.time_stamp = f.split('_', 2)[2].split('.')[0]


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


if __name__ == "__main__":
	count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	root = TrieNode('*')
	prelist = [
		"00",
		"10",
		"000",
		"010",
		"011",
		"100",
		"101",
		"110",
		"111",
		"0010",
		"0011",
		"0100",
		"0101",
		"0110",
		"1010",
		"1011",
		"1111",
		"00101",
		"00110",
		"00111",
		"01000",
		"11000",
		"11001",
		"11111",
		"001011",
		"110001",
		"110010",
		"0010111"]

	# with open("D:/x/act.txt") as fp:
	# 	for line in fp:
	# 		add(root,line)

	i=0
	for pr in prelist:

		add(root, pr,str(i))
		i += 1


	root.display()
	leafpush(root)
	root.display()
	# printPreorder(root)

	print('------------')
	lre=[]
	print(make_LRE(root,lre))
	print(lre)