import pandas as pd
import matplotlib.pyplot as plt
import os  # file muveletek
import datetime
from datetime import date
import time
import copy
import numpy as np
import itertools
import operator



class Save:
	time_stamp = ''
	msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	count = 0
	sum_msp = 0
	per8 = 0

	def __init__(self):
		self.time_stamp = ''
		self.msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.count = 0
		self.sum_msp = 0
		self.per8 = 0

	def blank_sheet(self):
		self.time_stamp = ''
		self.msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.count = 0
		self.sum_msp = 0
		self.per8 = 0


m = 4  # darab fib
n = 32  # 32 minden prefix hosszra


class Dev:
	time_stamp = ''
	msp_count = []
	pref_count = []
	count = []
	sum_msp = []
	per8 = []
	pref_avg = []
	msp_avg = []
	count_avg = 0
	sum_msp_avg = 0
	per8_avg = 0
	msp_stdev = []
	pref_stdev = []
	count_stdev = 0
	sum_msp_stdev = 0
	per8_stdev = 0

	def __init__(self):
		self.time_stamp = ''
		self.msp_count = []
		self.pref_count = []
		self.count = []
		self.sum_msp = []
		self.per8 = []
		self.pref_avg = []
		self.msp_avg = []
		self.count_avg = 0
		self.sum_msp_avg = 0
		self.per8_avg = 0
		self.msp_stdev = []
		self.pref_stdev = []
		self.count_stdev = 0
		self.sum_msp_stdev = 0
		self.per8_stdev = 0

	def blank_sheet(self):
		self.time_stamp = ''
		self.msp_count = []
		self.pref_count = []
		self.count = []
		self.sum_msp = []
		self.per8 = []
		self.pref_avg = []
		self.msp_avg = []
		self.count_avg = 0
		self.sum_msp_avg = 0
		self.per8_avg = 0
		self.msp_stdev = []
		self.pref_stdev = []
		self.count_stdev = 0
		self.sum_msp_stdev = 0
		self.per8_stdev = 0

	def tostring(self):
		str_pref_avg = ""
		for i in self.pref_avg:
			str_pref_avg += "," + str(i)
		str_pref_stdev = ""
		for i in self.pref_stdev:
			str_pref_stdev += "," + str(i)

		return str(self.time_stamp) + "," + str(self.count_avg) + "," + str(self.sum_msp_avg) + "," + str(self.count_stdev) + "," + str(self.sum_msp_stdev) +',pref_avg'+ str_pref_avg + ',pref_stdev' + str_pref_stdev


def read_in_csv(list, filepath):
	# 0	            1	        2	    3	    4	    5	    6	    7	    8	    9	    10	    11	    12	    13	    14	    15	    16	    17	    18	    19	    20	    21	    22	    23	    24	    25	    26	    27	    28	    29	    30	    31	    32	    33	    34	    35	  36	37	  38	39	  40	41	  42	43	  44	 45	    46	   47	  48	 49	    50	   51	  52	53	    54	   5      56	 57	    58	   59	  60	 61	    62	   63	  64	65	    66	   67
	# Date,         Total_count,Msp_sum,Pref_1, Pref_2, Pref_3, Pref_4, Pref_5, Pref_6, Pref_7, Pref_8, Pref_9, Pref_10,Pref_11,Pref_12,Pref_13,Pref_14,Pref_15,Pref_16,Pref_17,Pref_18,Pref_19,Pref_20,Pref_21,Pref_22,Pref_23,Pref_24,Pref_25,Pref_26,Pref_27,Pref_28,Pref_29,Pref_30,Pref_31,Pref_32,Msp_1,Msp_2,Msp_3,Msp_4,Msp_5,Msp_6,Msp_7,Msp_8,Msp_9,Msp_10,Msp_11,Msp_12,Msp_13,Msp_14,Msp_15,Msp_16,Msp_17,Msp_18,Msp_19,Msp_20,Msp_21,Msp_22,Msp_23,Msp_24,Msp_25,Msp_26,Msp_27,Msp_28,Msp_29,Msp_30,Msp_31,Msp_32,Per_8
	# 2013-11-13,   478068,     45241,  0,      0,      0,      0,      0,      0,      0,      16,     11,     31,     92,     253,    474,    925,    1629,   12802,  6757,   11183,  22958,  32763,  35487,  49533,  43724,  249120, 33,     60,     94,     93,     9013,   417,    148,    451,    0,    0,    0,    0,    0,    0,    0,    15,   9,    21,    65,    148,   264,   536,   760,   4314,  2453,  3867,  6029,  7751,  6694,  7032,  5200,  9,     3,     1,     4,     0,     66,    0,     0,     0,     158.22465646266937

	list.clear()
	with open(filepath) as fp:
		line = fp.readline()
		line = fp.readline()

		while line:
			wip = Save()
			wip.blank_sheet()
			line_parts = line.split(",")
			wip.time_stamp = line_parts[0]
			wip.count = int(line_parts[1])
			wip.sum_msp = int(line_parts[2])
			for i in range(3, 35):
				# print(line_parts[i])
				wip.pref_count[i - 3] = int(line_parts[i])
			for i in range(35, 67):
				# print(line_parts[i])
				wip.msp_count[i - 35] = int(line_parts[i])
			wip.per8 = float(line_parts[67].split('\n')[0])

			list.append(wip)
			line = fp.readline()

	fp.close()


def create_fib_list():
	for item in bme_List:
		# print("bme" + item.time_stamp)
		element = Dev()
		element.blank_sheet()
		element.time_stamp = item.time_stamp
		element.msp_count.append(item.msp_count)
		element.pref_count.append(item.pref_count)
		element.count.append(item.count)
		element.sum_msp.append(item.sum_msp)
		element.per8.append(item.per8)
		fib_List.append(element)

	# for fib in fib_List:
	# 	if '2013-12-04' in fib.time_stamp:
	# 		print ("van")
	# 		f_index = fib_List.index(fib)
	# 		print(f_index)

	f_index = 0
	new = True
	for item in szeged_List:
		# print("szeged" + item.time_stamp)
		new = True
		for fib in fib_List:
			if item.time_stamp in fib.time_stamp:
				f_index = fib_List.index(fib)
				new = False
				break
		if new:
			element = Dev()
			element.blank_sheet()
			element.time_stamp = item.time_stamp
			element.msp_count.append(item.msp_count)
			element.pref_count.append(item.pref_count)
			element.count.append(item.count)
			element.sum_msp.append(item.sum_msp)
			element.per8.append(item.per8)
			fib_List.append(element)
		else:
			fib_List[f_index].msp_count.append(item.msp_count)
			fib_List[f_index].pref_count.append(item.pref_count)
			fib_List[f_index].count.append(item.count)
			fib_List[f_index].sum_msp.append(item.sum_msp)
			fib_List[f_index].per8.append(item.per8)

	new = True
	for item in vh1_List:
		# print("vh1" + item.time_stamp)
		new = True
		for fib in fib_List:
			if item.time_stamp in fib.time_stamp:
				f_index = fib_List.index(fib)
				new = False
				break
		if new:
			element = Dev()
			element.blank_sheet()
			element.time_stamp = item.time_stamp
			element.msp_count.append(item.msp_count)
			element.pref_count.append(item.pref_count)
			element.count.append(item.count)
			element.sum_msp.append(item.sum_msp)
			element.per8.append(item.per8)
			fib_List.append(element)
		else:
			fib_List[f_index].msp_count.append(item.msp_count)
			fib_List[f_index].pref_count.append(item.pref_count)
			fib_List[f_index].count.append(item.count)
			fib_List[f_index].sum_msp.append(item.sum_msp)
			fib_List[f_index].per8.append(item.per8)

	new = True
	for item in vh2_List:
		new = True
		for fib in fib_List:
			if item.time_stamp in fib.time_stamp:
				f_index = fib_List.index(fib)
				new = False
				break
		if new:
			element = Dev()
			element.blank_sheet()
			element.time_stamp = item.time_stamp
			element.msp_count.append(item.msp_count)
			element.pref_count.append(item.pref_count)
			element.count.append(item.count)
			element.sum_msp.append(item.sum_msp)
			element.per8.append(item.per8)
			fib_List.append(element)
		else:
			fib_List[f_index].msp_count.append(item.msp_count)
			fib_List[f_index].pref_count.append(item.pref_count)
			fib_List[f_index].count.append(item.count)
			fib_List[f_index].sum_msp.append(item.sum_msp)
			fib_List[f_index].per8.append(item.per8)


def create_rib_list():
	for item in linx_List:
		# print("bme" + item.time_stamp)
		element = Dev()
		element.blank_sheet()
		element.time_stamp = item.time_stamp
		element.msp_count.append(item.msp_count)
		element.pref_count.append(item.pref_count)
		element.count.append(item.count)
		element.sum_msp.append(item.sum_msp)
		element.per8.append(item.per8)
		rib_List.append(element)

	f_index = 0
	new = True
	for item in kixp_List:
		# print("szeged" + item.time_stamp)
		new = True
		for rib in rib_List:
			if item.time_stamp in rib.time_stamp:
				f_index = rib_List.index(rib)
				new = False
				break
		if new:
			element = Dev()
			element.blank_sheet()
			element.time_stamp = item.time_stamp
			element.msp_count.append(item.msp_count)
			element.pref_count.append(item.pref_count)
			element.count.append(item.count)
			element.sum_msp.append(item.sum_msp)
			element.per8.append(item.per8)
			rib_List.append(element)
		else:
			rib_List[f_index].msp_count.append(item.msp_count)
			rib_List[f_index].pref_count.append(item.pref_count)
			rib_List[f_index].count.append(item.count)
			rib_List[f_index].sum_msp.append(item.sum_msp)
			rib_List[f_index].per8.append(item.per8)

	new = True
	for item in eqix_List:
		# print("vh1" + item.time_stamp)
		new = True
		for rib in rib_List:
			if item.time_stamp in rib.time_stamp:
				f_index = rib_List.index(rib)
				new = False
				break
		if new:
			element = Dev()
			element.blank_sheet()
			element.time_stamp = item.time_stamp
			element.msp_count.append(item.msp_count)
			element.pref_count.append(item.pref_count)
			element.count.append(item.count)
			element.sum_msp.append(item.sum_msp)
			element.per8.append(item.per8)
			rib_List.append(element)
		else:
			rib_List[f_index].msp_count.append(item.msp_count)
			rib_List[f_index].pref_count.append(item.pref_count)
			rib_List[f_index].count.append(item.count)
			rib_List[f_index].sum_msp.append(item.sum_msp)
			rib_List[f_index].per8.append(item.per8)

	new = True
	for item in sydney_List:
		# print("vh2" + item.time_stamp)
		new = True
		for rib in rib_List:
			if item.time_stamp in rib.time_stamp:
				f_index = rib_List.index(rib)
				new = False
				break
		if new:
			element = Dev()
			element.blank_sheet()
			element.time_stamp = item.time_stamp
			element.msp_count.append(item.msp_count)
			element.pref_count.append(item.pref_count)
			element.count.append(item.count)
			element.sum_msp.append(item.sum_msp)
			element.per8.append(item.per8)
			rib_List.append(element)
		else:
			rib_List[f_index].msp_count.append(item.msp_count)
			rib_List[f_index].pref_count.append(item.pref_count)
			rib_List[f_index].count.append(item.count)
			rib_List[f_index].sum_msp.append(item.sum_msp)
			rib_List[f_index].per8.append(item.per8)


def Average(lst):
	return sum(lst) / len(lst)


def calc_avg(lst):
	for day in lst:
		day.count_avg = Average(day.count)
		day.sum_msp_avg = Average(day.sum_msp)
		day.per8_avg = Average(day.per8)
		if len(day.msp_count) <= 1:
			for i in range(32):
				day.msp_avg.append(Average([day.msp_count[0][i]]))
		if len(day.msp_count) == 2:
			for i in range(32):
				day.msp_avg.append(Average([day.msp_count[0][i], day.msp_count[0][i]]))
		if len(day.msp_count) == 3:
			for i in range(32):
				day.msp_avg.append(Average([day.msp_count[0][i], day.msp_count[1][i], day.msp_count[2][i]]))
		if len(day.msp_count) == 4:
			for i in range(32):
				day.msp_avg.append(Average([day.msp_count[0][i], day.msp_count[1][i], day.msp_count[2][i], day.msp_count[3][i]]))
		if len(day.pref_count) <= 1:
			for i in range(32):
				day.pref_avg.append(Average([day.pref_count[0][i]]))
		if len(day.pref_count) == 2:
			for i in range(32):
				day.pref_avg.append(Average([day.pref_count[0][i], day.pref_count[0][i]]))
		if len(day.pref_count) == 3:
			for i in range(32):
				day.pref_avg.append(Average([day.pref_count[0][i], day.pref_count[1][i], day.pref_count[2][i]]))
		if len(day.pref_count) == 4:
			for i in range(32):
				day.pref_avg.append(Average([day.pref_count[0][i], day.pref_count[1][i], day.pref_count[2][i], day.pref_count[3][i]]))


def calc_std(lst):
	for day in lst:
		day.count_stdev = np.std(day.count)
		day.sum_msp_stdev = np.std(day.sum_msp)
		day.per8_stdev = np.std(day.per8)

		if len(day.msp_count) <= 1:
			for i in range(32):
				day.msp_stdev.append(np.std([day.msp_count[0][i]]))
		if len(day.msp_count) == 2:
			for i in range(32):
				day.msp_stdev.append(np.std([day.msp_count[0][i], day.msp_count[0][i]]))
		if len(day.msp_count) == 3:
			for i in range(32):
				day.msp_stdev.append(np.std([day.msp_count[0][i], day.msp_count[1][i], day.msp_count[2][i]]))
		if len(day.msp_count) == 4:
			for i in range(32):
				day.msp_stdev.append(np.std([day.msp_count[0][i], day.msp_count[1][i], day.msp_count[2][i], day.msp_count[3][i]]))
		if len(day.pref_count) <= 1:
			for i in range(32):
				day.pref_stdev.append(np.std([day.pref_count[0][i]]))
		if len(day.pref_count) == 2:
			for i in range(32):
				day.pref_stdev.append(np.std([day.pref_count[0][i], day.pref_count[0][i]]))
		if len(day.pref_count) == 3:
			for i in range(32):
				day.pref_stdev.append(np.std([day.pref_count[0][i], day.pref_count[1][i], day.pref_count[2][i]]))
		if len(day.pref_count) == 4:
			for i in range(32):
				day.pref_stdev.append(np.std([day.pref_count[0][i], day.pref_count[1][i], day.pref_count[2][i], day.pref_count[3][i]]))

		for i in day.msp_count:
			day.msp_stdev.append(np.std(i))
		for i in day.pref_count:
			day.pref_stdev.append(np.std(i))


'''
2 listát vár
és vissza adja a pár korelációját -1 +1 között
'''


def correlate(x, y):
	sx = 0
	xx = 0
	zx = []
	sy = 0
	xy = 0
	zy = []
	zxzy = []

	xx = Average(x)
	sx = np.std(x)
	for i in x:
		zx.append((i - xx) / sx)

	xy = Average(y)
	sy = np.std(y)
	for i in y:
		zy.append((i - xy) / sy)

	if len(x) < len(y):
		for i in range(len(x)):
			zxzy.append(zx[i] * zy[i])
		return (sum(zxzy)) / len(x)

	else:
		for i in range(len(y)):
			zxzy.append(zx[i] * zy[i])
		return (sum(zxzy)) / len(y)


bme_List = []
szeged_List = []
vh1_List = []
vh2_List = []
fib_List = []
linx_List = []
kixp_List = []
eqix_List = []
sydney_List = []
rib_List = []

if __name__ == "__main__":
	loc = "D:/Users/Baki/Documents/GitHub/IP-stats-trends/venv/csv/"
	f_bme = loc + 'bme.csv'
	f_szeged = loc + 'szeged.csv'
	f_vh1 = loc + 'vh1.csv'
	f_vh2 = loc + 'vh2.csv'
	f_linx = loc + 'linx.csv'
	f_kixp = loc + 'kixp.csv'
	f_eqix = loc + 'eqix.csv'
	f_sydney = loc + 'sydney.csv'

	read_in_csv(bme_List, f_bme)
	print("done bme list")
	read_in_csv(szeged_List, f_szeged)
	print("done szeged list")
	read_in_csv(vh1_List, f_vh1)
	print("done vh1 list")
	read_in_csv(vh2_List, f_vh2)
	print("done vh2 list")

	read_in_csv(linx_List, f_linx)
	print("done linx list")
	read_in_csv(kixp_List, f_kixp)
	print("done kixp list")
	read_in_csv(eqix_List, f_eqix)
	print("done eqix list")
	read_in_csv(sydney_List, f_sydney)
	print("done sydney list")

	bme = pd.read_csv(f_bme, parse_dates = ["Date"], index_col = "Date")
	linx = pd.read_csv(f_linx, parse_dates = ["Date"], index_col = "Date")

	for pair in itertools.product([f_bme,f_szeged,f_vh1,f_vh2], [f_linx,f_kixp,f_eqix,f_sydney]):
		# print (pair)
		fib = pd.read_csv(pair[0], parse_dates = ["Date"], index_col = "Date")
		rib = pd.read_csv(pair[1], parse_dates = ["Date"], index_col = "Date")
		for f_col,r_col in zip(fib.columns,rib. columns):
			# if f_col and r_col in ["Total_count", "Msp_sum", "Pref_8", "Pref_9", "Pref_10", "Pref_11", "Pref_12", "Pref_13", "Pref_14", "Pref_15", "Pref_16", "Pref_17", "Pref_18", "Pref_19", "Pref_20", "Pref_21", "Pref_22", "Pref_23", "Pref_24"]:
				f_list = fib[f_col].values.tolist()
				r_list = rib[r_col].values.tolist()
				print(pair[0].split("/")[-1].split(".")[0]+","+pair[1].split("/")[-1].split(".")[0]+","+f_col+ ","+str(correlate(f_list, r_list)))

	create_fib_list()
	print("done fib list")

	create_rib_list()
	print("done rib list")

	calc_avg(fib_List)
	calc_avg(rib_List)

	print("done average")

	calc_std(fib_List)
	calc_std(rib_List)

	print("done standard deviation")

	sorted_fib_List = sorted(fib_List, key = operator.attrgetter('time_stamp'))

	# with open("F:/cha6/fib_list_stat.txt",'w') as fp:
	# 	for day in sorted_fib_List:
	# 		fp.write(day.tostring()+'\n')
	# 	fp.close()

	print("###")
	print("###")
	print("###")
	print("###")

	sorted_rib_List = sorted(rib_List, key = operator.attrgetter('time_stamp'))

	# with open("F:/cha6/rib_list_stat.txt", 'w') as fp:
	# 	for day in sorted_rib_List:
	# 		fp.write(day.tostring() + '\n')
	# 	fp.close()

	print("end")

fib_sigma_count = 0
fib_avg_count = 0
fib_avg_list = []
z_fib = []

for day in fib_List:
	fib_avg_list.append(day.count_avg)
fib_avg_count = Average(fib_avg_list)
print(fib_avg_count)
fib_sigma_count = np.std(fib_avg_list)
print (fib_sigma_count)
for i in fib_avg_list:
	z_fib.append((i - fib_avg_count) / fib_sigma_count)

rib_sigma_count = 0
rib_avg_count = 0
rib_avg_list = []
z_rib = []

for day in rib_List:
	rib_avg_list.append(day.count_avg)
rib_avg_count = Average(rib_avg_list)
print(rib_avg_count)
rib_sigma_count = np.std(rib_avg_list)
print (rib_sigma_count)
for i in rib_avg_list:
	z_fib.append((i - rib_avg_count) / rib_sigma_count)

szum = []
for i in range(len(fib_avg_list)):
	x = fib_avg_list[i]
	y = rib_avg_list[i]
	szum.append(((x - fib_avg_count) / fib_sigma_count) * ((y - rib_avg_count) / rib_sigma_count))
print(sum(szum))
print((sum(szum)) / len(fib_avg_list))
