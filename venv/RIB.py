import os
import datetime
from multiprocessing import Pool, Lock
import re  # regex

# cd /mnt/c/teszt/rib
# cd /mnt/d/Users/Baki/Documents/GitHub/IP-stats-trends/venv
'''
otthoni
	cd /mnt/d/Users/Baki/Documents/GitHub/IP-stats-trends/venv
	/mnt/e/2019/
	E:/2019/
	/mnt/d/x/rib/
	/mnt/f/new_rib/
	F:/new_rib

'''
# https://manpages.debian.org/testing/bgpdump/bgpdump.1.en.html
# bgpdump rib.20190101.0000.bz2 -O 20190101.txt

source = 'kixp'
location ='/mnt/f/new_rib/' #'C:/rib_teszt/' '/mnt/f/new_rib/'   /mnt/c/teszt/rib/ C:/teszt/rib/
txt_location ='/mnt/c/rib_teszt/'#'C:/rib_teszt/'   '/mnt/c/rib_teszt/'
bz2_dir = source + '/'
txt_dir = source + '_rib_txt/'
fib_dir = source + '_rib_fib_format/'

teszt_file = 'rib_20131101.txt'  # rib_20131101.txt  rib.20131101.0000.bz2
rib_list = []
txt_list = []
out_list = []
pref = ''
next = ''
bz2_count = 0
bz2_current = 0


def init(l):
	global lock
	lock = l


def read_rib(rib_bz2_file):
	out_name = 'rib_' + rib_bz2_file.split('.')[1] + '.txt'
	myCmd = 'bgpdump ' + location + bz2_dir + rib_bz2_file + ' -O ' + txt_location + txt_dir + out_name
	print(myCmd)
	os.system(myCmd)
	return out_name


def convert_to_fib_format(rib_txt_file):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('{0}  by process id: {1} at: {2}'.format(rib_txt_file, proc, start_time))
	pref = ''
	next = ''
	out_list = []

	with open(txt_location + txt_dir + rib_txt_file) as fp:
		line = fp.readline()
		while line:
			if re.search('^PREFIX', line):
				pref = (line.split(' ')[1].strip())
			if re.search('^NEXT_HOP', line):
				next = (line.split(' ')[1].strip())
			line = fp.readline()
			if pref and next:
				if ':' not in pref:
					if len(out_list) == 0:
						out_list.append(pref + '\t' + next)
						pref = ''
						next = ''
					elif pref not in out_list[-1]:
						out_list.append(pref + '\t' + next)
						pref = ''
						next = ''
				else:
					break
	with open(location + fib_dir + source + '_' + rib_txt_file, 'w') as f:
		for i in out_list:
			f.write(str(i) + '\n')


def bz2_to_fib(rib_bz2_file):
	proc = os.getpid()
	start_time = datetime.datetime.now()

	print('Process ID: {0} \t at: {1} started read the file: {2}'.format(proc, start_time, rib_bz2_file))
	rib_txt_name = 'rib_' + rib_bz2_file.split('.')[1] + '.txt'

	if not os.path.isfile(location + fib_dir + source + '_' + rib_txt_name):
		rib_txt_file = read_rib(rib_bz2_file)
		global bz2_current
		bz2_current += 1
		print('Process ID: {0} \t at: {1} started convert the file: {2}\t({3}/{4})'.format(proc, datetime.datetime.now(), rib_bz2_file, bz2_current, bz2_count))
		convert_to_fib_format(rib_txt_file)
		os.remove(txt_location + txt_dir + rib_txt_file)
		print('Process ID: {0} \t at: {1} finished the file: {2}'.format(proc, datetime.datetime.now() - start_time, rib_bz2_file))
	else:
		print(rib_txt_name + '\t exist skipping')



if __name__ == "__main__":

	print(location + bz2_dir)
	for root, dirs, files in os.walk(location + bz2_dir):
		for file in files:
			if 'bz2' in file:
				rib_list.append(file)
	print(rib_list)

	bz2_count = len(rib_list)
	bz2_current = 0

	l = Lock()
	# pool = Pool(initializer = init, initargs = (l,), processes = os.cpu_count())
	pool = Pool(initializer = init, initargs = (l,), processes = 2)

	result = pool.map(bz2_to_fib, rib_list)
	pool.close()
	pool.join()
