import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
import datetime
from datetime import date
from prefixtree import TrieNode, add, sum_level
from multiprocessing import Process, Pool
import time

location = 'C:/fib data archive'
unzipLocation = location + '/extract/'
workFiles = []

storeList = []

vh1 = "^hbone_vh1"
vh2 = "^hbone_vh2"
bme = "^hbone_bme"
szeged = "^hbone_szeged"


class Save:
	time_stamp = ''
	prefixCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	count = 0

	def __init__(self):
		self.time_stamp = ''
		self.prefixCount = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
		                    0]
		self.count = 0

	"""
		Fájlba írja az osztályt
	"""

	def end_game(self, f):
		today = date.today().strftime("%y-%m-%d")
		file_name = location + '/save_' + str(f) + '_' + str(today) + '.txt'

		with open(file_name, 'a+') as f:
			# timestamp
			f.write("\n" + str(self.time_stamp))
			# prefix count
			f.write("\t" + str(self.count))
			# more specific prefixes
			for i in self.prefixCount:
				f.write("\t" + str(i))

			f.close()

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


"""
Csak a 4 full bgp fájlt tartja meg.
"""


def unzip():
	for root, dirs, files in os.walk(location):
		if files:
			loc = root + '/' + ''.join(files)
			# print(loc)
			workFiles.append(loc)

	for wF in workFiles:
		print('unzipping: ' + wF)
		with tarfile.open(wF) as f:
			f.extractall(unzipLocation)

		workingFiles = []
		for root, dirs, files in os.walk(unzipLocation):
			workingFiles = files
		for x in workingFiles:
			if not re.search(vh1, x) and not re.search(vh2, x) and not re.search(bme, x) and not re.search(szeged, x):
				delfile = unzipLocation + x
				# print('delete file: ' + delfile)
				os.remove(delfile)


def store_to_list(filepath, wip):  # első prefix tárolása default gatewayel

	tst = datetime.datetime.now()
	storeList.clear()
	with open(filepath) as fp:
		line = fp.readline()
		cnt = 1
		while line:
			# print("Line {}: {}".format(cnt, line.strip()))
			tmp = line.split("\t")
			tmp2 = tmp[0].split("/")
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
	wip.count = cnt
	print(str(datetime.datetime.now() - tst) + ' store end of file: ' + str(filepath))


def mp_work(file):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('{0}  by process id: {1} at: {2}'.format(file, proc,start_time))

	wip = Save()
	pre_tree_root = TrieNode('*')

	store_to_list(str(unzipLocation) + str(file), wip)
	wip.set_date(file)

	print("start tree " + str(unzipLocation) + str(file))
	st = datetime.datetime.now()
	print(st)

	for pr in storeList:
		add(pre_tree_root, pr.bin[0:int(pr.prefix)])
	print("end tree " + str(unzipLocation) + str(file))
	end = datetime.datetime.now()
	print(end - st)
	for i in range(0, 32):
		wip.prefixCount[i - 1] = sum_level(pre_tree_root, i)
	wip.end_game(file.split('_', 2)[1])
	end_time = datetime.datetime.now()
	print('{0}  by process id: {1} finished in: {2}'.format(file, proc, end_time-start_time))





if __name__ == "__main__":
	print('1: unzip')
	print('2: save more specific prefix')
	print('3: multiprocess test')
	print('4: do test')
	cmd = input('mi legyen?')
	if cmd == '1':
		unzip()

	if cmd == '2':
		sta = datetime.datetime.now()
		print("start program: " + str(sta))

		for root, dirs, files in os.walk(unzipLocation):
			if files:
				for file in files:
					if re.search(vh1, str(file)):
						wip = Save()
						pre_tree_root = TrieNode('*')

						store_to_list(str(root) + str(file), wip)
						wip.set_date(file)

						print("start tree" + str(root) + str(file))
						st = datetime.datetime.now()
						print(st)

						for pr in storeList:
							add(pre_tree_root, pr.bin[0:int(pr.prefix)])
						print("end tree" + str(root) + str(file))
						end = datetime.datetime.now()
						print(end - st)
						for i in range(0, 32):
							wip.prefixCount[i - 1] = sum_level(pre_tree_root, i)
						wip.end_game(file.split('_', 2)[1])

		print("full program program " + str(datetime.datetime.now() - sta))

	if cmd == '3':
		start = datetime.datetime.now()
		print("start program: " + str(start))

		in_files = []
		pool = Pool(processes = os.cpu_count())

		for root, dirs, files in os.walk(unzipLocation):
			if files:
				in_files=files

		result = pool.map(mp_work, in_files)
		print("full program program " + str(datetime.datetime.now() - start))

	if cmd == '4':
		loc = []
		for root, dirs, files in os.walk(unzipLocation):
			if files:
				for f in files:
					loc.append(str(root) + str(f))
			print(loc)
