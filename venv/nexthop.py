import pandas as pd
import matplotlib.pyplot as plt
import os  # file muveletek
import datetime
from datetime import date
import time
import copy
import numpy as np


class nHop:
	time_stamp = ''
	next_hop = ''
	count = 0
	per8 = 0
	adv_range = 0

	def __init__(self):
		self.time_stamp = ''
		self.next_hop = ''
		self.count = 0
		self.per8 = 0
		self.adv_range = 0

	def blank_sheet(self):
		self.time_stamp = ''
		self.next_hop = ''
		self.count = 0
		self.per8 = 0

	def tostring(self):
		return str(self.time_stamp) + "," + str(self.next_hop) + "," + str(self.count) + "," + str(self.per8) + "," + str(self.adv_range)


class Ip:
	time_stamp = ''
	address = 0
	prefix = 0
	nh = 0
	msp = 0
	bin = ''

	def __init__(self, address, prefix, nh):
		self.address = address
		self.prefix = prefix
		self.nh = nh

	def tostring(self):
		return str(self.bin) + '\t' + str(self.address) + '\t' + str(self.nh) + '\t' + str(self.prefix) + '\t' + str(
			self.msp)

	def write_pre_bin(self):
		return str(self.bin[0:int(self.prefix)])


def store_to_list(filepath):  # első prefix tárolása

	lst = []
	with open(filepath) as fp:
		line = fp.readline()
		# default gateway kihagyása
		if line[8] == '0':
			line = fp.readline()
		cnt = 1
		while line:
			# print("Line {}: {}".format(cnt, line.strip()))
			tmp = line.split("\t")
			tmp2 = tmp[0].split("/")

			p = Ip(tmp2[0], tmp2[1], tmp[1].strip())
			mydate= filepath.split("_")[-1].split('.')[0]
			p.time_stamp = mydate[0]+mydate[1]+mydate[2]+mydate[3]+'-'+mydate[4]+mydate[5]+'-'+mydate[6]+mydate[7]

			lst.append(p)
			cnt += 1
			line = fp.readline()
	fp.close()
	return lst


def calc_per8(per8):
	return (2 ** (32 - int(per8))) / (2 ** 24)


location = "C:/o"
workFiles = []
workList = []
hops = {}

if __name__ == "__main__":
	start = datetime.datetime.now()
	print('start ' + str(start))

	for root, dirs, files in os.walk(location):
		for file in files:
			if file.split('.')[-1] == 'txt':
				workFiles.append(root + '/' + file)
				print(root + '/' + file)

	# for filepath in workFiles:
	# 	store_to_list(filepath, workList)

	workList = store_to_list("F:/cha6/in/bme_fib_20191101.txt")

	for item in workList:
		if item.nh not in hops:
			hop = nHop()
			hop.time_stamp = item.time_stamp
			hop.next_hop = item.nh
			hop.count = 1
			hop.per8 = calc_per8(item.prefix)
			hop.adv_range = 2 ** (32 - int(item.prefix))
			hops[item.nh] = hop
		else:
			hop = nHop()
			hop.time_stamp = item.time_stamp
			hop.next_hop = item.nh
			hop.count = hops[item.nh].count + 1
			hop.per8 = hops[item.nh].per8 + calc_per8(item.prefix)
			hop.adv_range = hops[item.nh].adv_range + 2 ** (32 - int(item.prefix))
			hops[item.nh] = hop

	for hop in hops.values():
		print(hop.tostring())

	print('finished ' + str(datetime.datetime.now() - start))
