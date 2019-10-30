import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
import datetime
from datetime import date
from prefixtree import TrieNode, add, sum_level, count_first_letter
from multiprocessing import Pool, Lock
import time
import copy

location = 'C:/fib data archive/2019-01'
unzipLocation = location + '/extract/'
workFiles = []

storeList = []

vh1 = "^hbone_vh1"
vh2 = "^hbone_vh2"
bme = "^hbone_bme"
szeged = "^hbone_szeged"


def init(l):
	global lock
	lock = l


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

	"""
		Fájlba írja az osztályt
	"""

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

	def end_game(self, f):
		today = date.today().strftime("%y-%m-%d")
		file_name = location + '/save_' + str(f) + '_' + str(today) + '.txt'

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


"""
Csak a 4 full bgp fájlt tartja meg.
"""


def unzip(wF):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('Unzipping {0}  by process id: {1} at: {2}'.format(wF, proc, start_time))
	un_zipped = False
	tmp = wF.split("/")[3].split('.')[0].split('-')
	k = tmp[0] + '_' + tmp[1] + '_' + tmp[2]
	for root, dirs, files in os.walk(unzipLocation):
		if files:
			for file in files:
				if re.search(k, str(file)):
					un_zipped = True
					print('Already unzipped {0}'.format(wF))
					break
	if not un_zipped:
		with tarfile.open(wF) as f:
			f.extractall(unzipLocation)

		unzipped_files = []
		for root, dirs, files in os.walk(unzipLocation):
			unzipped_files = files
		for x in unzipped_files:
			if not re.search(vh1, x) and not re.search(vh2, x) and not re.search(bme, x) and not re.search(szeged, x):
				delfile = unzipLocation + x
				# print('delete file: ' + delfile)
				os.remove(delfile)


def unzip_single(wF):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('Unzipping {0}  by process id: {1} at: {2}'.format(wF, proc, start_time))

	# 'F:/fib_data_archive/2018\\2018-01-13_backup/2018-01-13.tar.xz'
	#                                    get this  ^^^^^^^^^^
	date = wF.split('/')[-1].split('.')[0]

	with tarfile.open(wF) as f:
		f.extractall(unzipLocation + date)

	unzipped_files = []
	result_files = []
	for root, dirs, files in os.walk(unzipLocation + date):
		unzipped_files = files
		result_files = copy.deepcopy(files)



	for x in unzipped_files:
		if not re.search(vh1, x) and not re.search(vh2, x) and not re.search(bme, x) and not re.search(szeged, x):
			delfile = unzipLocation + date + '/' + x
			# print('delete file: ' + delfile)
			os.remove(delfile)
			result_files.remove(x)

	return (date, result_files)

def delete_left_over(date,wFs):
	for x in wFs:
		delfile = unzipLocation + date + '/' + x
		os.remove(delfile)
	os.rmdir(unzipLocation + date)



def store_to_list(filepath, wip):  # első prefix tárolása

	tst = datetime.datetime.now()
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

			p = Ip(tmp2[0], tmp2[1], tmp[1].strip())
			prefix = tmp2[0].split(".")
			for i in prefix:
				p.bin += bin(int(i))[2:].zfill(8)
			if cnt == 1:
				storeList.append(p)

				# diagram 3 hoz prefix ek számolása
				wip.pref_count[int(tmp2[1].strip()) - 1] += 1

				cnt += 1

			if (cnt > 1 and not (storeList[storeList.__len__() - 1].address == p.address and storeList[
				storeList.__len__() - 1].prefix == p.prefix)):
				storeList.append(p)

				# diagram 3 hoz prefix ek számolása
				wip.pref_count[int(tmp2[1].strip()) - 1] += 1

				# print(storeList[cnt-1].address)
				cnt += 1
			line = fp.readline()
	wip.count = cnt
	print(str(datetime.datetime.now() - tst) + ' store end of file: ' + str(filepath))


def mp_work(file):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('{0}  by process id: {1} at: {2}'.format(file, proc, start_time))

	wip = Save()
	pre_tree_root = TrieNode('*')

	store_to_list(str(unzipLocation) + str(file), wip)
	wip.set_date(file)

	print("start tree " + str(unzipLocation) + str(file))

	for pr in storeList:
		add(pre_tree_root, pr.bin[0:int(pr.prefix)])
	print("end tree " + str(unzipLocation) + str(file))

	for i in range(0, 32):
		wip.msp_count[i - 1] = sum_level(pre_tree_root, i)

	wip.set_sum_msp()

	count_p8 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

	count_first_letter(pre_tree_root, 0, count_p8)
	for i in range(0, 32):
		wip.per8 += count_p8[i] * (1 / (2 ** (i - 7)))

	wip.end_game(file.split('_', 2)[1])
	end_time = datetime.datetime.now()
	print('{0}  by process id: {1} finished in: {2}'.format(file, proc, end_time - start_time))


def mp_work_single(file):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('{0}  by process id: {1} at: {2}'.format(file, proc, start_time))

	unzippedWithDate = unzip_single(file)
	date = unzippedWithDate[0]
	unzipped = unzippedWithDate[1]

	wip = Save()
	pre_tree_root = TrieNode('*')

	for file in unzipped:
		wip.blank_sheet()
		store_to_list(str(unzipLocation) + str(date) + '/' + str(file), wip)
		wip.set_date(file)

		print("start tree " + str(unzipLocation) + str(file))

		for pr in storeList:
			add(pre_tree_root, pr.bin[0:int(pr.prefix)])
		print("end tree " + str(unzipLocation) + str(file))

		for i in range(0, 32):
			wip.msp_count[i - 1] = sum_level(pre_tree_root, i)

		wip.set_sum_msp()

		count_p8 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		count_first_letter(pre_tree_root, 0, count_p8)
		for i in range(0, 32):
			wip.per8 += count_p8[i] * (1 / (2 ** (i - 7)))

		lock.acquire()
		wip.end_game(file.split('_', 2)[1])
		lock.release()
		end_time = datetime.datetime.now()
	delete_left_over(date,unzipped)
	print('{0}  by process id: {1} finished in: {2}'.format(file, proc, end_time - start_time))


if __name__ == "__main__":
	print('start: just jump into it')
	print('1: unzip')
	print('1.1: unzip single file')
	print('2: save more specific prefix')
	print('3: multiprocess test')
	print('4: lock test')
	print('5: do test')
	cmd = input('mi legyen?')
	if cmd == '1':
		for root, dirs, files in os.walk(location):
			if files:
				loc = root + '/' + ''.join(files)
				# print(loc)
				workFiles.append(loc)

	# pool = Pool(processes = os.cpu_count())
	# result = pool.map(unzip, workFiles)

	if cmd == 'start':
		for root, dirs, files in os.walk(location):
			for file in files:
				if file.split('.')[-1] == 'xz':
					workFiles.append(root + '/' + file)

	# pool = Pool(initializer = init, initargs = (l,), processes = os.cpu_count())
	pool = Pool(processes = 1)
	result = pool.map(mp_work_single, workFiles)
	pool.close()
	pool.join()

	if cmd == '1.1':
		s = input('file')
		with tarfile.open(s) as f:
			f.extractall(unzipLocation)

		unzipped_files = []
		for root, dirs, files in os.walk(unzipLocation):
			unzipped_files = files
		for x in unzipped_files:
			if not re.search(vh1, x) and not re.search(vh2, x) and not re.search(bme, x) and not re.search(szeged, x):
				delfile = unzipLocation + x
				# print('delete file: ' + delfile)
				os.remove(delfile)

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
							wip.msp_count[i - 1] = sum_level(pre_tree_root, i)
						wip.end_game(file.split('_', 2)[1])

		print("full program program " + str(datetime.datetime.now() - sta))

	if cmd == '3':
		start = datetime.datetime.now()
		print("start program: " + str(start))

		in_files = []
		pool = Pool(processes = os.cpu_count())

		for root, dirs, files in os.walk(unzipLocation):
			if files:
				in_files = files

		result = pool.map(mp_work, in_files)
		print("full program program " + str(datetime.datetime.now() - start))

	if cmd == '4':
		loc = []
		for root, dirs, files in os.walk(unzipLocation):
			if files:
				for f in files:
					loc.append(str(root) + str(f))
			print(loc)

	if cmd == '5':
		wip = Save()
		pre_tree_root = TrieNode('*')

		file = "F:/2019/extract/hbone_vh1_2019_06_07_00_27_03.txt"
		store_to_list(file, wip)
		wip.set_date(file)

		st = datetime.datetime.now()

		for pr in storeList:
			add(pre_tree_root, pr.bin[0:int(pr.prefix)])

		end = datetime.datetime.now()
		print(end - st)
		for i in range(0, 32):
			wip.msp_count[i - 1] = sum_level(pre_tree_root, i)

		wip.set_sum_msp()

		count_p8 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

		count_first_letter(pre_tree_root, 0, count_p8)
		for i in range(0, 32):
			wip.per8 += count_p8[i] * (1 / (2 ** (i - 7)))

		wip.end_game(file.split('_', 2)[1])
