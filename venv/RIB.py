import os
import datetime
from multiprocessing import Pool
import re  # regex

# cd /mnt/c/users/bakit/PycharmProjects/IP-stats-trends/venv
# cd /mnt/c/teszt/rib
# https://manpages.debian.org/testing/bgpdump/bgpdump.1.en.html
# bgpdump rib.20190101.0000.bz2 -O 20190101.txt

location = 'C:/teszt/rib/'  # '/mnt/c/teszt/rib/'

file = 'rib_20131101.txt'  # rib_20131101.txt  rib.20131101.0000.bz2
rib = []
out_list = []


def read_rib(rib_file):
	out_name = 'rib_' + rib_file.split('.')[1] + '.txt'
	myCmd = 'bgpdump ' + location + rib_file + ' -O ' + location + out_name
	print(myCmd)
	os.system(myCmd)


def convert_to_fib_format(rib_txt):
	with open(location + rib_txt) as fp:
		line = fp.readline()

		if re.search('^PREFIX', line):
			pref = (line.split(' ')[1])
		if re.search('^NEXT_HOP', line):
			next = (line.split(' ')[1])

		out_list.append(pref + '\t' + next)


if __name__ == "__main__":

	# for root, dirs, files in os.walk(location):
	# 	rib = files
	#
	# pool = Pool(processes = os.cpu_count())
	# result = pool.map(read_rib, rib)

	pref = ''
	next = ''
	with open(location + file) as fp:
		line = fp.readline()
		while line:
			if re.search('^PREFIX', line):
				pref = (line.split(' ')[1])
			if re.search('^NEXT_HOP', line):
				next = (line.split(' ')[1])

		out_list.append(pref + '\t' + next)

	with open(location + 'kesz_' + file, 'w') as f:
		for i in out_list:
			f.write(str(i) + "\n")
