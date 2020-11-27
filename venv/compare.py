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
import numpy as np

out_location = 'D:/x/compare/'
rle_location = 'D:/x/rle/'
two32=2**32
today = datetime.date.today().strftime("%y-%m-%d")

if __name__ == "__main__":
	for root, dirs, files in os.walk(rle_location):
		for file in files:
			print(file)

	for a, b in itertools.combinations(files, 2):
		a_lst = []
		b_lst = []
		a_nh = []
		b_nh = []
		name_a = a.split("_")[0]
		name_b = b.split("_")[0]
		out_name = name_a + "_" + name_b + "_" + today + ".txt"
		print(name_a, name_b)

		with open(rle_location + a) as fpa:
			for line in fpa:  # ['0', 768]
				nh = line.split("\'")[1]
				count = line[:-2].split(" ")[1]
				if nh in a_nh:
					nh_i = a_nh.index(nh)
				else:
					a_nh.append(nh)
					nh_i = a_nh.index(nh)
				element = [nh_i, int(count)]
				a_lst.append(element)
		fpa.close()
		with open(out_location + name_a + "_nexthops.txt", 'w+') as f:
			for i in a_nh:
				f.write(str(i) + '\n')
		f.close()
		with open(rle_location + b) as fpb:
			for line in fpb:  # ['0', 768]
				nh = line.split("\'")[1]
				count = line[:-2].split(" ")[1]
				if nh in b_nh:
					nh_i = b_nh.index(nh)
				else:
					b_nh.append(nh)
					nh_i = b_nh.index(nh)
				element = [nh_i, int(count)]
				b_lst.append(element)
		fpb.close()
		with open(out_location + name_b + "_nexthops.txt", 'w+') as f:
			for i in b_nh:
				f.write(str(i) + '\n')
		f.close()

		c = np.zeros([a_nh.__len__(), b_nh.__len__()])
		# print(c[80][110])
		i = 0
		j = 0
		while (True):
			if a_lst[i][1] == b_lst[j][1]:
				c[a_lst[i][0]][b_lst[j][0]] += a_lst[i][1]
				# print("[" + str(a_lst[i][0]) + "," +str(b_lst[j][0])+"] "+ str(b_lst[j][1]))
				if i < a_lst.__len__()-1 and j < b_lst.__len__()-1:
					i += 1
					j += 1
				else:
					break
			if a_lst[i][1] < b_lst[j][1]:
				b_lst[j][1] = (b_lst[j][1] - a_lst[i][1])
				c[a_lst[i][0]][b_lst[j][0]] += a_lst[i][1]
				# print("[" + str(a_lst[i][0]) + "," +str(b_lst[j][0])+"] "+ str(a_lst[i][1]))
				if i < a_lst.__len__()-1:
					i += 1
				else:
					break
			if a_lst[i][1] > b_lst[j][1]:
				a_lst[i][1] = (a_lst[i][1] - b_lst[j][1])
				c[a_lst[i][0]][b_lst[j][0]] += b_lst[j][1]
				# print("["+str(a_lst[i][0])+","+str(b_lst[j][0])+"] "+ str(b_lst[j][1]))
				if j < b_lst.__len__()-1:
					j += 1
				else:
					break
			# print("i: "+str(i)+"\tj: "+str(j))
		print(len(a_lst))
		print(len(b_lst))
		for i in range(len(a_nh)):
			for j in range(len(b_nh)):
				c[i][j]= c[i][j]/two32
		# %d
		np.savetxt(out_location+out_name, c,fmt='%10.11f', delimiter = '\t')
		break
