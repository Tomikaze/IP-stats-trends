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
			date = date_element[0] + date_element[1] + date_element[2]
			# print(date)
			line_parts[0] = date
			# print(line)
			out_list.append('\t'.join(line_parts))
			line = fp.readline()

	fp.close()
	with open(filepath, "w") as fp:
		for line in out_list:
			fp.write(line)
	fp.close


def reformat_data_to_csv(filepath, file):
	# 0	                    1	            2	    3	        4	    5	        6	7	8	9	10	11	12	13	14	15	16	17	18	19	20	    21	    22	    23	    24	    25	    26	    27	    28	    29	    30	31	32	33	34	    35	36	37	38	        39	40	41	42	43	44	45	46	47	48	49	50	51	52	53	54	    55	    56	    57	    58	    59	    60	    61	    62	63	64	65	66	67	68	69	70	71	    72
	# 2013_12_25_23_59_59	total_count:	477591	msp_sum:	45839	pref_count:	0	0	0	0	0	0	0	16	11	31	92	253	473	941	1642	12833	6777	11226	23102	33056	35728	50318	43995	251571	34	58	96	91	4444	408	151	243	msp_count:	0	0	0	0	0	0	0	15	9	21	65	145	265	547	765	4363	2483	3864	6052	7842	6831	7164	5328	13	4	1	4	0	58	0	0	0	per 8:	158.58484077453613
	header = "Date:	Total_count	Msp_sum	Pref_1	Pref_2	Pref_3	Pref_4	Pref_5	Pref_6	Pref_7	Pref_8	Pref_9	Pref_10	Pref_11	Pref_12	Pref_13	Pref_14	Pref_15	Pref_16	Pref_17	Pref_18	Pref_19	Pref_20	Pref_21	Pref_22	Pref_23	Pref_24	Pref_25	Pref_26	Pref_27	Pref_28	Pref_29	Pref_30	Pref_31	Pref_32	Msp_1	Msp_2	Msp_3	Msp_4	Msp_5	Msp_6	Msp_7	Msp_8	Msp_9	Msp_10	Msp_11	Msp_12	Msp_13	Msp_14	Msp_15	Msp_16	Msp_17	Msp_18	Msp_19	Msp_20	Msp_21	Msp_22	Msp_23	Msp_24	Msp_25	Msp_26	Msp_27	Msp_28	Msp_29	Msp_30	Msp_31	Msp_32	Per_8\n"
	header_parts = header.split("\t")
	header = ','.join(header_parts)
	print(header)
	out_list = []
	storeList.clear()
	with open(filepath + file) as fp:
		line = fp.readline()
		# line = fp.readline()

		while line:
			# print("Line {}: {}".format(cnt, line.strip()))
			line_parts = line.split("\t")
			line_parts.remove("total_count:")
			line_parts.remove("msp_sum:")
			line_parts.remove("pref_count:")
			line_parts.remove("msp_count:")
			line_parts.remove("per 8:")
			# print(','.join(line_parts))
			out_list.append(','.join(line_parts))
			line = fp.readline()

	fp.close()
	file = file.split('.')[0] + ".csv"
	with open(filepath + file, "w") as fp:
		fp.write(header)
		for line in out_list:
			fp.write(line)
	fp.close


def reformat_csv_date(filepath, file):
	out_list = []
	storeList.clear()
	with open(filepath + file) as fp:
		line = fp.readline()
		line = fp.readline()

		while line:
			# print("Line {}: {}".format(cnt, line.strip()))
			line_parts = line.split(",", 1)
			date = line_parts[0]
			new_date = date[0] + date[1] + date[2] + date[3] + '-' + date[4] + date[5] + '-' + date[6] + date[7]
			out_list.append(new_date + ',' + line_parts[1])
			line = fp.readline()

	fp.close()
	with open(filepath + '/a/' + file, "w") as fp:
		header = "Date	Total_count	Msp_sum	Pref_1	Pref_2	Pref_3	Pref_4	Pref_5	Pref_6	Pref_7	Pref_8	Pref_9	Pref_10	Pref_11	Pref_12	Pref_13	Pref_14	Pref_15	Pref_16	Pref_17	Pref_18	Pref_19	Pref_20	Pref_21	Pref_22	Pref_23	Pref_24	Pref_25	Pref_26	Pref_27	Pref_28	Pref_29	Pref_30	Pref_31	Pref_32	Msp_1	Msp_2	Msp_3	Msp_4	Msp_5	Msp_6	Msp_7	Msp_8	Msp_9	Msp_10	Msp_11	Msp_12	Msp_13	Msp_14	Msp_15	Msp_16	Msp_17	Msp_18	Msp_19	Msp_20	Msp_21	Msp_22	Msp_23	Msp_24	Msp_25	Msp_26	Msp_27	Msp_28	Msp_29	Msp_30	Msp_31	Msp_32	Per_8\n"
		header_parts = header.split("\t")
		header = ','.join(header_parts)
		fp.write(header)
		for line in out_list:
			fp.write(line)
	fp.close


def get_full_date():
	for y in range(3, 10):
		for m in range(1, 13):
			if (y == 3 and (m == 11 or m == 12)) or (y == 9 and (
					m == 1 or m == 2 or m == 3 or m == 4 or m == 5 or m == 6)) or y == 4 or y == 5 or y == 6 or y == 7 or y == 8:
				for d in range(1, 32):

					if m == 2 and d < 29:
						if m < 10:
							mo = '0' + str(m)
						else:
							mo = str(m)
						if d < 10:
							da = '0' + str(d)
						else:
							da = str(d)
						# print("201"+str(y) + ' ' + str(mo) + ' ' + str(da))
						full_date_list.append("201" + str(y) + '-' + str(mo) + '-' + str(da))

					if (m == 4 or m == 6 or m == 9 or m == 11) and d < 31:
						if m < 10:
							mo = '0' + str(m)
						else:
							mo = str(m)
						if d < 10:
							da = '0' + str(d)
						else:
							da = str(d)
						# print("201"+str(y) + ' ' + str(mo) + ' ' + str(da))
						full_date_list.append("201" + str(y) + '-' + str(mo) + '-' + str(da))

					if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
						if m < 10:
							mo = '0' + str(m)
						else:
							mo = str(m)
						if d < 10:
							da = '0' + str(d)
						else:
							da = str(d)
						# print("201"+str(y) + ' ' + str(mo) + ' ' + str(da))
						full_date_list.append("201" + str(y) + '-' + str(mo) + '-' + str(da))


def append_csv_by_source(src_filepath, src_file):
	with open(src_filepath + src_file) as sfp:
		line = sfp.readline()
		line = sfp.readline()

		while line:
			out_list.append(line)
			line = sfp.readline()
	sfp.close()


def write_file(dest_filepath, dst_file):
	out_list.sort()
	with open(dest_filepath + dst_file, "a+") as dfp:
		header = "Date	Total_count	Msp_sum	Pref_1	Pref_2	Pref_3	Pref_4	Pref_5	Pref_6	Pref_7	Pref_8	Pref_9	Pref_10	Pref_11	Pref_12	Pref_13	Pref_14	Pref_15	Pref_16	Pref_17	Pref_18	Pref_19	Pref_20	Pref_21	Pref_22	Pref_23	Pref_24	Pref_25	Pref_26	Pref_27	Pref_28	Pref_29	Pref_30	Pref_31	Pref_32	Msp_1	Msp_2	Msp_3	Msp_4	Msp_5	Msp_6	Msp_7	Msp_8	Msp_9	Msp_10	Msp_11	Msp_12	Msp_13	Msp_14	Msp_15	Msp_16	Msp_17	Msp_18	Msp_19	Msp_20	Msp_21	Msp_22	Msp_23	Msp_24	Msp_25	Msp_26	Msp_27	Msp_28	Msp_29	Msp_30	Msp_31	Msp_32	Per_8\n"
		header_parts = header.split("\t")
		header = ','.join(header_parts)
		dfp.write(header)
		for line in out_list:
			dfp.write(line)
	dfp.close()
	out_list.clear()


def store_to_df():
	print("send help")


workFiles = []
storeList = []
full_date_list = []
out_list = []

if __name__ == "__main__":
	# source= "eqix"
	# ix = ['jinx', 'linx', 'sydney', 'eqix']
	# location = 'F:/Fib_done/RIB'
	# dest_loc = 'F:/Fib_done/'
	# dst_file = source+".csv"
	#
	# for root, dirs, files in os.walk(location):
	# 	for file in files:
	# 		if file.split('.')[-1] == 'csv':
	# 			if source in file:
	# 				workFiles.append(root + '/' + file)
	# 				append_csv_by_source(root + '/', file)
	# 				print(file)
	# write_file(dest_loc, dst_file)

	bme = pd.read_csv("F:/Fib_done/bme.csv", parse_dates = ["Date"], index_col = "Date")

	for i in range(48, 95):
		plot = bme.iloc[i * 20:i * 20 + 1].mean().plot(
			y = ['Pref_8', 'Pref_9', 'Pref_10', 'Pref_11', 'Pref_12', 'Pref_13', 'Pref_14', 'Pref_15', 'Pref_16', 'Pref_17', 'Pref_18', 'Pref_19', 'Pref_20', 'Pref_21', 'Pref_22', 'Pref_23',
			     'Pref_24', 'Pref_25', 'Pref_26', 'Pref_27', 'Pref_28', 'Pref_29', 'Pref_30', 'Pref_31', 'Pref_32'], figsize = (40, 20), kind = "pie")
		# plot.set_yscale('log')
		plot.set_ylim([0, 500000])
		fig = plot.get_figure()
		fig.savefig("F:/kep/"+str(i) + ".png")


# get_full_date()

# pd.read_csv("F:/Fib_done/FIB/2013_save_bme_19-11-03.csv")
# print(pd)

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
