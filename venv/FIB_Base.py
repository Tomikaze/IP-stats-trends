import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
import datetime
from datetime import date
from prefixtree import TrieNode, add, sum_level, count_first_letter
from multiprocessing import Pool, Lock
import time
import copy

all = ['2019/']  # '2014/', '2015/', '2016/', '2017/', '2018/', '2019/']
location = 'D:/TomiKJ/orig/fib_data_archive/'  # /mnt/fib_archive/     F:/fib_data_archive/    F:\rib_linx_fib_format/     /mnt/rib_linx_fib_format/     D:/TomiKJ/orig/fib_data_archive1
rib_save_loc = '/mnt/'  # /mnt/   F:/

workFiles = []

storeList = []

vh1 = "^hbone_vh1"
vh2 = "^hbone_vh2"
bme = "^hbone_bme"
szeged = "^hbone_szeged"
rib = "_rib_"


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
		file_name = save_loc + '_'+ save_name + '_' + str(today) + '.csv'

		with open(file_name, 'a+') as f:
			# append header if empty
			if (os.stat(file_name).st_size == 0):
				header = "Date	Total_count	Msp_sum	Pref_1	Pref_2	Pref_3	Pref_4	Pref_5	Pref_6	Pref_7	Pref_8	Pref_9	Pref_10	Pref_11	Pref_12	Pref_13	Pref_14	Pref_15	Pref_16	Pref_17	Pref_18	Pref_19	Pref_20	Pref_21	Pref_22	Pref_23	Pref_24	Pref_25	Pref_26	Pref_27	Pref_28	Pref_29	Pref_30	Pref_31	Pref_32	Msp_1	Msp_2	Msp_3	Msp_4	Msp_5	Msp_6	Msp_7	Msp_8	Msp_9	Msp_10	Msp_11	Msp_12	Msp_13	Msp_14	Msp_15	Msp_16	Msp_17	Msp_18	Msp_19	Msp_20	Msp_21	Msp_22	Msp_23	Msp_24	Msp_25	Msp_26	Msp_27	Msp_28	Msp_29	Msp_30	Msp_31	Msp_32	Per_8"
				header_parts = header.split("\t")
				header = ','.join(header_parts)
				f.write(header)

			# timestamp
			print(self.time_stamp)
			date = self.time_stamp[0] + self.time_stamp[1] + self.time_stamp[2] + self.time_stamp[3] + '-' + self.time_stamp[5] + self.time_stamp[6] + '-' + self.time_stamp[8] + self.time_stamp[9]
			print(date)
			f.write("\n" + date)

			# Total prefix count 1. diagram
			f.write("," + str(self.count))

			# sum more specific prefix count 2. diagram
			f.write("," + str(self.sum_msp))

			# prefix count by length 3. diagram
			for i in self.pref_count:
				f.write("," + str(i))

			# more specific prefix count by length 4. diagram
			for i in self.msp_count:
				f.write("," + str(i))

			# per 8 range 5. diagram
			f.write("," + str(self.per8))

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


def unzip_single(wF):
	# 'F:/fib_data_archive/2018\\2018-01-13_backup/2018-01-13.tar.xz'
	#                                    get this  ^^^^^^^^^^
	date = wF.split('/')[-1].split('.')[0]
	unzipLocation = wF.rsplit('/', 2)[0] + '_extract/'
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


def log_mp_work_err(loc, error, filename):
	today = datetime.date.today().strftime("%y-%m-%d")
	file_name = loc + '_error_' + str(filename) + '_' + str(today) + '.txt'

	lock.acquire()
	with open(file_name, 'a+') as f:
		time = datetime.datetime.now()
		f.write(error + '\t' + filename + '\t' + str(time) + '\n')
		f.close()
	lock.release()


def delete_left_over(unzipLocation, date, wFs):
	for x in wFs:
		delfile = unzipLocation + date + '/' + x
		os.remove(delfile)
	os.rmdir(unzipLocation + date)


def store_to_list(filepath, wip):  # első prefix tárolása

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



def mp_work_single(file):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('Process ID: {0} \t at: {1} started file: {2}'.format(proc, start_time, file))
	unzipLocation = file.rsplit('/', 2)[0] + '_extract/'
	try:
		unzipped_with_date = unzip_single(file)
		end_unzip_time = datetime.datetime.now()
		print('Process ID: {0} \t at: {1} unzipped file: {2}'.format(proc, end_unzip_time, file))
		date = unzipped_with_date[0]
		unzipped = unzipped_with_date[1]

		for file in unzipped:
			wip = Save()
			pre_tree_root = TrieNode('*')
			wip.blank_sheet()
			store_to_list(str(unzipLocation) + str(date) + '/' + str(file), wip)
			wip.set_date(file)

			start_tree_time = datetime.datetime.now()
			for pr in storeList:
				add(pre_tree_root, pr.bin[0:int(pr.prefix)])
			end_tree_time = datetime.datetime.now()
			print('Process ID: {0} \t at: {1} finished TREE: {2} in: {3}'.format(proc, end_tree_time, file, end_tree_time - start_tree_time))

			for i in range(0, 32):
				wip.msp_count[i - 1] = sum_level(pre_tree_root, i)

			wip.set_sum_msp()

			count_p8 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

			count_first_letter(pre_tree_root, 0, count_p8)
			for i in range(0, 32):
				wip.per8 += count_p8[i] * (1 / (2 ** (i - 7)))


			lock.acquire()
			wip.end_game(unzipLocation + file)
			lock.release()
		end_time = datetime.datetime.now()
		delete_left_over(unzipLocation, date, unzipped)
	except Exception as e:
		log_mp_work_err(location, e, file)
		print(e)
		print(file)

	print('Process ID: {0} \t at: {1} finished file: {2} in: {3}'.format(proc, end_time, file, end_time - start_time))



if __name__ == "__main__":
	for date in all:
		for root, dirs, files in os.walk(location + date):
			for file in files:
				if file.split('.')[-1] == 'xz':
					workFiles.append(root + '/' + file)
					print(file)

	l = Lock()
	pool = Pool(initializer = init, initargs = (l,), processes = os.cpu_count())
	# pool = Pool(initializer = init, initargs = (l,), processes = 1)
	result = pool.map(mp_work_single, workFiles)
	pool.close()
	pool.join()