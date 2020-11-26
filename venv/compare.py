import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
import datetime
from datetime import date
from multiprocessing import Pool, Lock
import time
import copy
from operator import itemgetter
import itertools

out_location = 'D:/TomiKJ/x/compare/'
rle_location = 'D:/TomiKJ/x/rle/'

today = datetime.date.today().strftime("%y-%m-%d")

if __name__ == "__main__":
	for root, dirs, files in os.walk(rle_location):
		for file in files:
			print(file)

	for a, b in itertools.combinations(files, 2):
		a_lst = []
		b_lst = []
		name_a = a.split("_")[0]
		name_b = b.split("_")[0]
		out_name = name_a + "_" + name_b + "_" + today + ".txt"
		print(name_a, name_b)

		with open(rle_location + a) as fpa:
			for line in fpa:  # ['*', 768]
				nh = line.split("\'")[1]
				count = line[:-2].split(" ")[1]
				element = [nh, int(count)]
				a_lst.append(element)
		fpa.close()
		with open(rle_location + a) as fpb:
			for line in fpa:  # ['*', 768]
				nh = line.split("\'")[1]
				count = line[:-2].split(" ")[1]
				element = [nh, int(count)]
				b_lst.append(element)
		fpb.close()
