import os
import datetime
from multiprocessing import Pool, Lock
import re  # regex

# cd /mnt/c/users/bakit/PycharmProjects/IP-stats-trends/venv
# cd /mnt/c/teszt/rib
# https://manpages.debian.org/testing/bgpdump/bgpdump.1.en.html
# bgpdump rib.20190101.0000.bz2 -O 20190101.txt

location = 'C:/teszt/rib/'  # '/mnt/c/teszt/rib/'
bz2 = 'rib_bz2/'
txt = 'rib_txt/'
fib = 'rib_fib/'

file = 'rib_20131101.txt'  # rib_20131101.txt  rib.20131101.0000.bz2
rib = []
out_list = []
pref = ''
next = ''


def init(l):
	global lock
	lock = l


def read_rib(rib_bz2_file):
	out_name = 'rib_' + rib_bz2_file.split('.')[1] + '.txt'
	myCmd = 'bgpdump ' + location + bz2 + rib_bz2_file + ' -O ' + location + txt + out_name
	print(myCmd)
	os.system(myCmd)


def convert_to_fib_format(rib_txt_file):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('{0}  by process id: {1} at: {2}'.format(rib_txt_file, proc, start_time))
	pref = ''
	next = ''
	with open(location + txt + rib_txt_file) as fp:
		line = fp.readline()
		while line:
			if re.search('^PREFIX', line):
				pref = (line.split(' ')[1].strip())
			if re.search('^NEXT_HOP', line):
				next = (line.split(' ')[1].strip())
			line = fp.readline()
			if pref and next:
				if ':' not in pref:
					out_list.append(pref + '\t' + next)
					pref = ''
					next = ''
				else:
					break

	lock.acquire()
	with open(location + fib + 'kesz_' + rib_txt_file, 'w') as f:
		for i in out_list:
			f.write(str(i) + '\n')

	lock.release()


if __name__ == "__main__":

	for root, dirs, files in os.walk(location + txt):
		rib = files

	pool = Pool(initializer = init, initargs = (l,), processes = os.cpu_count())
	result = pool.map(convert_to_fib_format, rib)
	pool.close()
	pool.join()
