from multiprocessing import Pool, Lock
from datetime import date
import datetime
import time
import os


def init(l):
	global lock
	lock = l


def f(i):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('process id: {0} \t created \t\t at: {1}'.format(proc, start_time))

	lock.acquire()
	lock_time = datetime.datetime.now()
	print('process id: {0} \t lock acquired \t at: {1}'.format(proc, lock_time))
	lock.release()


if __name__ == '__main__':
	l = Lock()
	pool = Pool(initializer = init, initargs = (l,), processes = os.cpu_count())
	pool.map(f, range(10))
	pool.close()
	pool.join()
