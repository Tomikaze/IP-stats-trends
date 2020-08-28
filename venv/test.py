import os  # file műveletek
import tarfile  # tar unzip
import re  # regex
import datetime
from datetime import date
from prefixtree import TrieNode, add, sum_level, count_first_letter
from multiprocessing import Pool, Lock
import time
import copy
import random
import numpy as np
import statistics
from fractions import Fraction as fr

# location = 'F:/fib_data_archive/2014/'  # /mnt/fib_archive/2013
#
# for root, dirs, files in os.walk(location):
# 	for file in files:
# 		if file.split('.')[-1] == 'xz':
# 			print(str(file))

# all = ['2013/', '2014/', '2016/', '2017/', '2018/', '2019/']
# location = 'F:/fib_data_archive/'  # /mnt/fib_archive/     F:/fib_data_archive/
# unzipLocation = 'F:/fib_data_archive/2013/2013-11-12_backup/2013-11-12.tar.xz'
# f = '/mnt/fib_archive/2014_extract/hbone_vh2_2014_05_18_00_32_46.txt'

# for year in all:
# 	for root, dirs, files in os.walk(location + year):
# 		for file in files:
# 			if file.split('.')[-1] == 'xz':
# 				print(root + '/' + file)
#
# print(str(unzipLocation.rsplit('/',2)[0]))
#
# save_loc = f.rsplit('_', 8)[0]
# save_name = f.rsplit('_')[-7]
# today = date.today().strftime("%y-%m-%d")
# print(today)
# file_name = save_loc + '_save_' + save_name + '_' + str(today) + '.txt'
# print(file_name)

# lst= []
# for o in range(10,20):
# 	b=[]
# 	for i in range(6):
# 		b.append(str(o)+str(i))
# 	lst.append(b)
# print(lst)
#
class BstNode:

    def __init__(self, key):
        self.key = key
        self.right = None
        self.left = None

    def insert(self, key):
        if self.key == key:
            return
        elif self.key < key:
            if self.right is None:
                self.right = BstNode(key)
            else:
                self.right.insert(key)
        else: # self.key > key
            if self.left is None:
                self.left = BstNode(key)
            else:
                self.left.insert(key)

    def display(self):
        lines, *_ = self._display_aux()
        for line in lines:
            print(line)

    def _display_aux(self):
        """Returns list of strings, width, height, and horizontal coordinate of the root."""
        # No child.
        if self.right is None and self.left is None:
            line = '%s' % self.key
            width = len(line)
            height = 1
            middle = width // 2
            return [line], width, height, middle

        # Only left child.
        if self.right is None:
            lines, n, p, x = self.left._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s
            second_line = x * ' ' + '/' + (n - x - 1 + u) * ' '
            shifted_lines = [line + u * ' ' for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, n + u // 2

        # Only right child.
        if self.left is None:
            lines, n, p, x = self.right._display_aux()
            s = '%s' % self.key
            u = len(s)
            first_line = s + x * '_' + (n - x) * ' '
            second_line = (u + x) * ' ' + '\\' + (n - x - 1) * ' '
            shifted_lines = [u * ' ' + line for line in lines]
            return [first_line, second_line] + shifted_lines, n + u, p + 2, u // 2

        # Two children.
        let, n, p, x = self.left._display_aux()
        riht, m, q, y = self.right._display_aux()
        s = '%s' % self.key
        u = len(s)
        first_line = (x + 1) * ' ' + (n - x - 1) * '_' + s + y * '_' + (m - y) * ' '
        second_line = x * ' ' + '/' + (n - x - 1 + u + y) * ' ' + '\\' + (m - y - 1) * ' '
        if p < q:
            let += [n * ' '] * (q - p)
        elif q < p:
            riht += [m * ' '] * (p - q)
        zipped_lines = zip(let, riht)
        lines = [first_line, second_line] + [a + u * ' ' + b for a, b in zipped_lines]
        return lines, n + m + u, max(p, q) + 2, n + u // 2


import random

b = BstNode(20)
for _ in range(20):
    b.insert(random.randint(0, 100))
b.display()

