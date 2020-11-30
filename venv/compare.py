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
import math
from typing import Any

out_location = 'D:/TomiKJ/x/teszt_compare/'
rle_location = 'D:/TomiKJ/x/rle/'
two32 = 2 ** 32
today = datetime.date.today().strftime("%y-%m-%d")

if __name__ == "__main__":
	for root, dirs, files in os.walk(rle_location):
		for file in files:
			print(file)

	'''
	Összes kombináció megadása
	'''
	for a, b in itertools.combinations(files, 2):
		a_lst = []
		b_lst = []
		a_nh = []
		b_nh = []
		name_a = a.split("_")[0]
		name_b = b.split("_")[0]
		out_name = name_a + "_" + name_b + "_" + today + ".txt"
		print(name_a, name_b)

		''' első file beolvasása tömb be'''
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
		''' első nexthopok kiírása'''
		with open(out_location + name_a + "_nexthops.txt", 'w+') as f:
			for i in a_nh:
				f.write(str(i) + '\n')
		f.close()
		''' második file beolvasása tömb be'''
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
		''' második file beolvasása tömb be'''
		with open(out_location + name_b + "_nexthops.txt", 'w+') as f:
			for i in b_nh:
				f.write(str(i) + '\n')
		f.close()

		''' elsőxmasodik as mátrix'''
		c = np.zeros([a_nh.__len__(), b_nh.__len__()])
		# print(c[80][110])

		''' konkrét black magic
		ha egyenlő akkor
		a mx a[i] b[i] eleméhez hozzá adja a lefedett prefix darabot
		  ha van hova növel mind2 listán
		  
		ha az egyik kisebb
		a nagyobb ból kivonja a kisebb lefedett prefix darabot
		a mx a[i] b[i] eleméhez hozzá adja a kisebb prefix darabot
		  növeli a kisebbet ha van hova
		'''
		i = 0
		j = 0
		while (True):
			if a_lst[i][1] == b_lst[j][1]:
				c[a_lst[i][0]][b_lst[j][0]] += a_lst[i][1]
				# print("[" + str(a_lst[i][0]) + "," +str(b_lst[j][0])+"] "+ str(b_lst[j][1]))
				if i < a_lst.__len__() - 1 and j < b_lst.__len__() - 1:
					i += 1
					j += 1
				else:
					break
			if a_lst[i][1] < b_lst[j][1]:
				b_lst[j][1] = (b_lst[j][1] - a_lst[i][1])
				c[a_lst[i][0]][b_lst[j][0]] += a_lst[i][1]
				# print("[" + str(a_lst[i][0]) + "," +str(b_lst[j][0])+"] "+ str(a_lst[i][1]))
				if i < a_lst.__len__() - 1:
					i += 1
				else:
					break
			if a_lst[i][1] > b_lst[j][1]:
				a_lst[i][1] = (a_lst[i][1] - b_lst[j][1])
				c[a_lst[i][0]][b_lst[j][0]] += b_lst[j][1]
				# print("["+str(a_lst[i][0])+","+str(b_lst[j][0])+"] "+ str(b_lst[j][1]))
				if j < b_lst.__len__() - 1:
					j += 1
				else:
					break
		# print("i: "+str(i)+"\tj: "+str(j))

		''' a konkrét darabos mx kiírása '''
		np.savetxt(out_location + "darab_mx_" + out_name, c, fmt = '%d', delimiter = '\t')

		''' leosztom 2**32 vel és annak a kiírása '''
		cn = np.zeros([a_nh.__len__(), b_nh.__len__()])
		for i in range(len(a_nh)):
			for j in range(len(b_nh)):
				cn[i][j] = c[i][j] / two32
		# %d   %10.11f
		np.savetxt(out_location + "norm_mx_" + out_name, cn, fmt = '%10.15f', delimiter = '\t')

		'''a file'''
		pd = []
		p = []

		for i in range(len(a_nh)):
			pdi = 0
			pi = 0
			for j in range(len(b_nh)):
				pdi += c[i][j]
				pi += cn[i][j]
			# print (c[i][j])
			# print("-----------")
			pd.append(pdi)
			p.append(pi)
		print("darab: " + str(pd))
		print("darab/2**32: " + str(p))
		h = []

		for i in range(0, len(p)):
			h.append(-1 * p[i] * math.log2(p[i]))
			# print(str(-1 * p[i] * math.log2(p[i])))
		print("egy forrás entropiája -pi*log2(pi): " + str(h))
		print("log2 n max H érték: " + str(math.log2(len(a_nh))))
		H = sum(h)
		print(" 0. elememel Entropia H: " + str(H))
		h = []
		for i in range(1, len(p)):
			h.append(-1 * p[i] * math.log2(p[i]))
		H = sum(h)
		print("0. elem nélküli Entropia H: " + str(H))

		'''b file'''
		pd = []
		p = []
		for i in range(len(b_nh)):
			pdi = 0
			pi = 0
			for j in range(len(a_nh)):
				pdi += c[j][i]
				pi += cn[j][i]
			# print (c[i][j])
			# print("-----------")
			pd.append(pdi)
			p.append(pi)
		print("darab: " + str(pd))
		print("darab/2**32: " + str(p))
		h = []
		for i in range(0, len(p)):
			h.append(-1 * p[i] * math.log2(p[i]))
			# print(str(-1 * p[i] * math.log2(p[i])))
		print("egy forrás entropiája -pi*log2(pi): " + str(h))
		print("log2 n max H érték: " + str(math.log2(len(a_nh))))
		H = sum(h)
		print(" 0. elememel Entropia H: " + str(H))
		h = []
		for i in range(1, len(p)):
			h.append(-1 * p[i] * math.log2(p[i]))
		H = sum(h)
		print("0. elem nélküli Entropia H: " + str(H))



		break
