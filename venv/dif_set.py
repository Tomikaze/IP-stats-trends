import pandas as pd
import matplotlib.pyplot as plt
import os  # file muveletek
import datetime
from datetime import date
import time
import copy
import numpy as np


class Save:
	time_stamp = ''
	msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	diff_to_prev_date = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
	count = 0
	sum_msp = 0
	adv_range = 0
	per8 = 0

	def __init__(self):
		self.time_stamp = ''
		self.msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		diff_to_prev_date = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.count = 0
		self.sum_msp = 0
		self.adv_range = 0
		self.per8 = 0

	def blank_sheet(self):
		self.time_stamp = ''
		self.msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		diff_to_prev_date = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.count = 0
		self.sum_msp = 0
		self.adv_range = 0
		self.per8 = 0

	"""
		Fájlba írja az osztályt
	"""


def write_diff_set_csv(list, f):
	save_name = f.rsplit('/')[-1]
	file_name = "F:/cha6/" + 'diff_set_' + save_name
	with open(file_name, "w") as fp:
		header = "Date  diff_prev_1	diff_prev_2	diff_prev_3	diff_prev_4	diff_prev_5	diff_prev_6	diff_prev_7	diff_prev_8	diff_prev_9	diff_prev_10	diff_prev_11	diff_prev_12	diff_prev_13	diff_prev_14	diff_prev_15	diff_prev_16	diff_prev_17	diff_prev_18	diff_prev_19	diff_prev_20	diff_prev_21	diff_prev_22	diff_prev_23	diff_prev_24	diff_prev_25	diff_prev_26	diff_prev_27	diff_prev_28	diff_prev_29	diff_prev_30	diff_prev_31	diff_prev_32\n"
		header_parts = header.split("\t")
		header = ','.join(header_parts)

		fp.write(header)
		for item in storeList:
			# timestamp
			fp.write(str(item.time_stamp))

			for i in item.diff_to_prev_date:
				fp.write("," + str(i))
			fp.write('\n')
	fp.close()

	def set_date(self, f):
		self.time_stamp = f.split('_', 2)[2].split('.')[0]
		print(self.time_stamp)


def read_in_csv(filepath):
	# 0	            1	        2	    3	    4	    5	    6	    7	    8	    9	    10	    11	    12	    13	    14	    15	    16	    17	    18	    19	    20	    21	    22	    23	    24	    25	    26	    27	    28	    29	    30	    31	    32	    33	    34	    35	  36	37	  38	39	  40	41	  42	43	  44	 45	    46	   47	  48	 49	    50	   51	  52	53	    54	   5      56	 57	    58	   59	  60	 61	    62	   63	  64	65	    66	   67
	# Date,         Total_count,Msp_sum,Pref_1, Pref_2, Pref_3, Pref_4, Pref_5, Pref_6, Pref_7, Pref_8, Pref_9, Pref_10,Pref_11,Pref_12,Pref_13,Pref_14,Pref_15,Pref_16,Pref_17,Pref_18,Pref_19,Pref_20,Pref_21,Pref_22,Pref_23,Pref_24,Pref_25,Pref_26,Pref_27,Pref_28,Pref_29,Pref_30,Pref_31,Pref_32,Msp_1,Msp_2,Msp_3,Msp_4,Msp_5,Msp_6,Msp_7,Msp_8,Msp_9,Msp_10,Msp_11,Msp_12,Msp_13,Msp_14,Msp_15,Msp_16,Msp_17,Msp_18,Msp_19,Msp_20,Msp_21,Msp_22,Msp_23,Msp_24,Msp_25,Msp_26,Msp_27,Msp_28,Msp_29,Msp_30,Msp_31,Msp_32,Per_8
	# 2013-11-13,   478068,     45241,  0,      0,      0,      0,      0,      0,      0,      16,     11,     31,     92,     253,    474,    925,    1629,   12802,  6757,   11183,  22958,  32763,  35487,  49533,  43724,  249120, 33,     60,     94,     93,     9013,   417,    148,    451,    0,    0,    0,    0,    0,    0,    0,    15,   9,    21,    65,    148,   264,   536,   760,   4314,  2453,  3867,  6029,  7751,  6694,  7032,  5200,  9,     3,     1,     4,     0,     66,    0,     0,     0,     158.22465646266937

	storeList.clear()
	with open(filepath) as fp:
		line = fp.readline()
		line = fp.readline()

		while line:
			wip = Save()
			wip.blank_sheet()
			line_parts = line.split(",")
			wip.time_stamp = line_parts[0]

			for i in range(3, 35):
				# print(line_parts[i])
				wip.pref_count[i - 3] = line_parts[i]

			storeList.append(wip)
			line = fp.readline()

	fp.close()


storeList = []

if __name__ == "__main__":
	loc = "D:/Users/Baki/Documents/GitHub/IP-stats-trends/venv/csv/"
	file = 'bme.csv'
	read_in_csv(loc+file)

	c = 0
	for i in range(len(storeList)):
		if i != 0:
			asd = []
			for j in range(len(storeList[i].pref_count)):
				asd.append(int(storeList[i].pref_count[j]) - int(storeList[i - 1].pref_count[j]))
			storeList[i].diff_to_prev_date = copy.deepcopy(asd)

	write_diff_set_csv(storeList, file)
