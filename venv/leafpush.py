import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
import datetime
from datetime import date
from prefixtree import TrieNode, add, sum_level, count_first_letter, leafpush, printPreorder, maxDepth, make_pushed_list
from multiprocessing import Pool, Lock
import time
import copy
from operator import itemgetter

location = 'D:/x'
fib_location= 'D:/x/fib_format'
workFiles = []
storeList = []
today = datetime.date.today().strftime("%y-%m-%d")


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
	print("start")

	# prelist = [
	# 	"00",
	# 	"10",
	#
	# 	"010",
	# 	"011",
	# 	"100",
	# 	"101",
	# 	"110",
	# 	"111",
	#
	#
	# 	"0100",
	# 	"0101",
	# 	"0110",
	# 	"1010",
	# 	"1011",
	# 	"1111",
	#
	# 	"01000",
	# 	"11000",
	# 	"11001",
	# 	"11111",
	#
	# 	"110001",
	# 	"110010",
	# 	]
	# i=0
	# for pr in prelist:
	#
	# 	add(root, pr,str(i))
	# 	i += 1
	# root.display()
	# leafpush(root)
	# root.display()
	# printPreorder(root)
	# pushed_list = []
	# make_pushed_list(root, pushed_list)
	# print(pushed_list)

	for roots, dirs, files in os.walk(fib_location):
		for file in files:
			print(file)
			start_time = datetime.datetime.now()
			root = TrieNode('*')
			print("file read start: " + str(start_time))
			with open(fib_location +"/"+ file) as fp:
				for line in fp:
					pr_bin = ""
					tmp = line.split("\t")
					tmp2 = tmp[0].split("/")
					pre_len = tmp2[1]
					prefix = tmp2[0].split(".")
					for i in prefix:
						pr_bin += bin(int(i))[2:].zfill(8)
					pr_bin = pr_bin[0:int(pre_len)]
					add(root, pr_bin, tmp[1].strip())

			print("file read end:" + str(datetime.datetime.now()))

			# root.display()
			print("leafpush start:" + str(datetime.datetime.now()))
			leafpush(root)
			print("leafpush end" + str(datetime.datetime.now()))

			# root.display()
			# printPreorder(root)

			print('------------')
			print("push list start" + str(datetime.datetime.now()))
			pushed_list = []
			make_pushed_list(root, pushed_list)
			print("push list end" + str(datetime.datetime.now()))
			# print(pushed_list)

			ordered = sorted(pushed_list, key = itemgetter(0))

			push_list_name = location + '/lp_list/' + file.split(".")[0] + '_pushed_list' + '_' + str(today) + '.txt'

			with open(push_list_name, 'w+') as f:
				for i in ordered:
					f.write(str(i) + '\n')

			# printPreorder(root)
			print('------------')
			print("RLE start" + str(datetime.datetime.now()))
			rle = []
			pre_end = 0
			pre_nh = "0"
			for i in ordered:
				full_bin = i[0].ljust(32, "0")
				full_range = str(bin(int(i[1], 10)))[2:].rjust(32, "0")
				cur_start = int(full_bin, 2)
				cur_end = int(i[0].ljust(32, "0"), 2) + int(i[1], 10)
				range = str(bin(int(i[1], 10)))[2:].rjust(32, "0")
				# print(cur_start)
				# print(full_bin)
				# print(range)
				# print(cur_end)
				if pre_end == cur_start:
					list_element = [i[2], int(i[1])]
					rle.append(list_element)
					pre_end = cur_end
				else:
					gap = cur_start - pre_end
					list_element = ["0", gap]
					rle.append(list_element)
					list_element = [i[2], int(i[1])]
					rle.append(list_element)
					pre_end = cur_end

			last = 2 ** 32
			gap = last - pre_end
			list_element = ["0", gap]
			rle.append(list_element)

			rle_name = location +"/rle/"+ file.split(".")[0] + '_rle' + '_V2_' + str(today) + '.txt'
			with open(rle_name, 'w+') as f:
				for i in rle:
					f.write(str(i) + '\n')

			print("RLE end " + str(datetime.datetime.now()))
			print("delta " + str(datetime.datetime.now() - start_time))
