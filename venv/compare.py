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

out_location = 'G:/cha6/compare_2019/'
rle_location = 'G:/cha6/rle_2019/'
two32 = 2 ** 32
today = datetime.date.today().strftime("%y-%m-%d")

if __name__ == "__main__":
	a_files = []
	b_files = []
	for root, dirs, files in os.walk(rle_location):
		for file in files:
			if "bme" in file or "szeged" in file or "vh1" in file or "vh2" in file:
				a_files.append(file)
			else:
				b_files.append(file)
	files = []
	files.append(a_files)
	files.append(b_files)
	'''
	Összes kombináció megadása
	'''
	for e in itertools.product(*files):
		a = e[0]
		b = e[1]
		a_lst = []
		b_lst = []
		a_nh = []
		b_nh = []
		name_a = a.split("_")[0]
		name_b = b.split("_")[0]
		out_name = name_a + "_" + name_b + "_" + today + ".txt"
		# print(name_a, name_b)

		''' FIB file beolvasása tömb be'''
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
		''' FIB nexthopok kiírása'''
		with open(out_location + name_a + "_nexthops.txt", 'w+') as f:
			for i in a_nh:
				f.write(str(i) + '\n')
		f.close()
		''' RIB file beolvasása tömb be'''
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
		''' RIB file beolvasása tömb be'''
		with open(out_location + name_b + "_nexthops.txt", 'w+') as f:
			for i in b_nh:
				f.write(str(i) + '\n')
		f.close()

		''' FIBxRIB as mátrix'''
		c = np.zeros([a_nh.__len__(), b_nh.__len__()])
		# print(c[80][110])

		''' 
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
		np.savetxt(out_location + name_a + "_" + name_b + "_" + "darab_mx_" + today + ".txt", c, fmt = '%d', delimiter = '\t')

		''' leosztom 2**32 vel és annak a kiírása '''
		cn = np.zeros([a_nh.__len__(), b_nh.__len__()])
		for i in range(len(a_nh)):
			for j in range(len(b_nh)):
				cn[i][j] = c[i][j] / two32
		# %d   %10.11f
		np.savetxt(out_location + name_a + "_" + name_b + "_" + "norm_mx_" + today + ".txt", cn, fmt = '%10.15f', delimiter = '\t')

		'''FIB stat file'''
		pd = []
		pa = []

		for i in range(len(a_nh)):
			pdi = 0
			pi = 0
			for j in range(len(b_nh)):
				pdi += c[i][j]
				pi += cn[i][j]
			# print (c[i][j])
			# print("-----------")
			pd.append(pdi)
			pa.append(pi)
		# print("darab: " + str(pd))
		# print("darab/2**32: " + str(p))
		ha = []  # entropia lista
		for i in range(0, len(pa)):
			ha.append(-1 * pa[i] * math.log2(pa[i]))
		# print(str(-1 * p[i] * math.log2(p[i])))
		# print("egy forrás entropiája -pi*log2(pi): " + str(h))
		# print("log2 n max H érték: " + str(math.log2(len(a_nh))))
		Ha = sum(ha)
		# print(" 0. elememel Entropia H: " + str(Ha))
		# hna = []
		# for i in range(1, len(p)):
		# 	hna.append(-1 * p[i] * math.log2(p[i]))
		# Hna= sum(hna)
		# print("0. elem nélküli Entropia H: " + str(Ha))

		'''RIB stat file'''
		pd = []
		pb = []
		for i in range(len(b_nh)):
			pdi = 0
			pi = 0
			for j in range(len(a_nh)):
				pdi += c[j][i]
				pi += cn[j][i]
			# print (c[i][j])
			# print("-----------")
			pd.append(pdi)
			pb.append(pi)
		# print("darab: " + str(pd))
		# print("darab/2**32: " + str(p))
		hb = []
		for i in range(0, len(pb)):
			hb.append(-1 * pb[i] * math.log2(pb[i]))
		# print(str(-1 * p[i] * math.log2(p[i])))
		# print("egy forrás entropiája -pi*log2(pi): " + str(h))
		# print("log2 n max H érték: " + str(math.log2(len(a_nh))))
		Hb = sum(hb)
		# print(" 0. elememel Entropia H: " + str(Hb))
		# hnb = []
		# for i in range(1, len(p)):
		# 	hnb.append(-1 * p[i] * math.log2(p[i]))
		# Hnb = sum(hb)
		# print("0. elem nélküli Entropia H: " + str(Hnb))


		# 5 leggyakoribb nexhop cím valószínűsége
		pa.sort(reverse = True)
		pb.sort(reverse = True)
		print('perem eloszlás', name_a, name_b)
		for i in range(5):
			print(pa[i],',', pb[i])
		#
		# print('entrópia')
		print('entrópia,', name_a,',', Ha,',', str(math.log2(len(a_nh))))
		print('entrópia,', name_b,',', Hb,',', str(math.log2(len(b_nh))))
		#
		# print('feltételes entrópia')
		HAB = 0
		cn[0][0]=0
		# for j in range(len(b_nh)):
		# 	for i in range(len(a_nh)):
		# 		log = cn[i][j] / pb[j]
		# 		# print(log)
		# 		if log != 0:
		# 			HAB += -1 * cn[i][j] * math.log2(log)

		print('feltételes entrópia',',',name_a,name_b,',',HAB)
		print('független:,',Ha+Hb)
		print('meghatározott 0 vagy',Ha,Hb)
		print('kölcsönös érték', name_a, name_b,',', Ha - HAB)
	# break
