import pandas as pd
import matplotlib.pyplot as plt
import os  # file műveletek
import datetime
from datetime import date
import time
import copy
import numpy as np


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
		self.msp_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.pref_count = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.count = 0
		self.sum_msp = 0
		self.adv_range = 0
		self.per8 = 0

	def set_date(self, f):
		self.time_stamp = f.split('_', 2)[2].split('.')[0]


def unify(filepath):
	# 0	                    1	            2	    3	        4	    5	        6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	    21	    22	    23	    24	    25	    26	    27	    28	    29	    30	31	32	33	34	    35	36	37	38	        39	40	41	42	43	44	45	46	47	48	49	50	51	52	53	54	    55	    56	    57	    58	    59	    60	    61	    62	63	64	65	66	67	68	69	70	71	    72
	# 2013_12_25_23_59_59	total_count:	477591	msp_sum:	45839	pref_count:	0	0	0	0	0	0	0	16	11	31	92	253	473	941	1642	12833	6777	11226	23102	33056	35728	50318	43995	251571	34	58	96	91	4444	408	151	243	msp_count:	0	0	0	0	0	0	0	15	9	21	65	145	265	547	765	4363	2483	3864	6052	7842	6831	7164	5328	13	4	1	4	0	58	0	0	0	per 8:	158.58484077453613
	out_list = []
	storeList.clear()
	with open(filepath) as fp:
		line = fp.readline()
		line = fp.readline()

		while line:
			# print("Line {}: {}".format(cnt, line.strip()))
			line_parts = line.split("\t")
			date_element = line_parts[0].split("_")
			# print(date_element)
			date=date_element[0]+date_element[1]+date_element[2]
			# print(date)
			line_parts[0]=date
			# print(line)
			out_list.append('\t'.join(line_parts))
			line = fp.readline()

	fp.close()
	with open(filepath, "w") as fp:
		for line in out_list:
			fp.write(line)
	fp.close


def

	# 		for i in prefix:
	# 			p.bin += bin(int(i))[2:].zfill(8)
	# 		if cnt == 1:
	# 			storeList.append(p)
	#
	# 			# diagram 3 hoz prefix ek számolása
	# 			wip.pref_count[int(tmp2[1].strip()) - 1] += 1
	#
	# 			cnt += 1
	#
	# 		if (cnt > 1 and not (storeList[storeList.__len__() - 1].address == p.address and storeList[
	# 			storeList.__len__() - 1].prefix == p.prefix)):
	# 			storeList.append(p)
	#
	# 			# diagram 3 hoz prefix ek számolása
	# 			wip.pref_count[int(tmp2[1].strip()) - 1] += 1
	#
	# 			# print(storeList[cnt-1].address)
	# 			cnt += 1
	# 		line = fp.readline()
	# wip.count = cnt


workFiles = []
storeList = []


if __name__ == "__main__":

	location = 'F:/Fib_done/FIB'
	for root, dirs, files in os.walk(location):
		for file in files:
			if file.split('.')[-1] == 'txt':
				if "bme" in file:
					workFiles.append(root + '/' + file)
					print(file)




# data = np.array(['a', 'b', 'c', 'd'])
# s = pd.Series(data)
# print(s)
#
# data = {'apples': [3, 2, 0, 1], 'oranges': [0, 3, 7, 2]}
#
# purchases = pd.DataFrame(data, index = ['June', 'Robert', 'Lily', 'David'])
#
# print(purchases.loc['June'])
# print(purchases)
#
# df = pd.DataFrame(np.random.randn(10, 4), index = pd.date_range('1/1/2000', periods = 10), columns = list('ABCD'))
#
# df.plot()
#
# Data = {'Unemployment_Rate': [6.1, 5.8, 5.7, 5.7, 5.8, 5.6, 5.5, 5.3, 5.2, 5.2], 'Stock_Index_Price': [1500, 1520, 1525, 1523, 1515, 1540, 1545, 1560, 1555, 1565]}
#
# df = pd.DataFrame(Data, columns = ['Unemployment_Rate', 'Stock_Index_Price'])
# df.plot(x = 'Unemployment_Rate', y = 'Stock_Index_Price', kind = 'scatter')
# print(df)
