import urllib.request, urllib.error
from multiprocessing import Pool, Lock
import os  # file műveletek
import datetime
from datetime import date

ix = ['kixp']  # 'linx', 'sydney', 'eqix'

# url = 'http://archive.routeviews.org/route-views.linx/bgpdata/2013.11/RIBS/rib.20131101.0000.bz2' #http://archive.routeviews.org/route-views.saopaulo/bgpdata/2020.12/RIBS/rib.20201201.0000.bz2
#        http://archive.routeviews.org/route-views.kixp/bgpdata/2014.07/RIBS/rib.20140701.0000.bz2
# file = 'F:/route views linx/rib.20131101.0000.bz2'
# C:/teszt/DL_teszt/rib_    /mnt/rib_   F:/new rib
file_root_loc = 'F:/new_rib/'
dloadlist = []
mo = ''
da = ''


def init(l):
	global lock
	lock = l


def log_dl_err(loc, error, filename):
	lock.acquire()
	with open(loc + 'error.txt', 'a+') as f:
		time = datetime.datetime.now()
		f.write(error + '\t' + filename + '\t' + str(time) + '\t' + '\n')
		f.close()
	lock.release()


def dload(url):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('{0}  by process id: {1} at: {2}'.format(url, proc, start_time))

	file_name = url.split('/')[7]
	current_ix = url.split('/')[3].split('.')[1]
	print(file_name, current_ix, file_root_loc + current_ix + '/' + file_name)
	try:
		if not os.path.isfile(file_root_loc + current_ix + '/' + file_name):
			with urllib.request.urlopen(url) as response, open(file_root_loc + current_ix + '/' + file_name, 'wb') as out_file:
				data = response.read()  # a `bytes` object
				out_file.write(data)
	except urllib.error.URLError as e:
		print(e.reason)
		log_dl_err(file_root_loc + current_ix + '/', e.reason, file_name)

	end_time = datetime.datetime.now()
	print('{0}  by process id: {1} finished in: {2}'.format(url, proc, end_time - start_time))


if __name__ == "__main__":

	for y in range(13, 21):     #2013 tól 2021 ig
		for m in range(1, 13):
			if (y == 13 and m >= 11) or y >= 14:    #2013 ból csak 11., 12. hónap kell
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
						print(str(y) + ' ' + str(mo) + ' ' + str(da))
						for i in ix:
							dloadlist.append('http://archive.routeviews.org/route-views.' + i + '/bgpdata/20' + str(y) + '.' + str(mo) + '/RIBS/rib.20' + str(y) + str(mo) + str(da) + '.0000.bz2')
					if (m == 4 or m == 6 or m == 9 or m == 11) and d < 31:
						if m < 10:
							mo = '0' + str(m)
						else:
							mo = str(m)
						if d < 10:
							da = '0' + str(d)
						else:
							da = str(d)
						print(str(y) + ' ' + str(mo) + ' ' + str(da))
						for i in ix:
							dloadlist.append('http://archive.routeviews.org/route-views.' + i + '/bgpdata/20' + str(y) + '.' + str(mo) + '/RIBS/rib.20' + str(y) + str(mo) + str(da) + '.0000.bz2')
					if m == 1 or m == 3 or m == 5 or m == 7 or m == 8 or m == 10 or m == 12:
						if m < 10:
							mo = '0' + str(m)
						else:
							mo = str(m)
						if d < 10:
							da = '0' + str(d)
						else:
							da = str(d)
						print(str(y) + ' ' + str(mo) + ' ' + str(da))
						for i in ix:
							dloadlist.append('http://archive.routeviews.org/route-views.' + i + '/bgpdata/20' + str(y) + '.' + str(mo) + '/RIBS/rib.20' + str(y) + str(mo) + str(da) + '.0000.bz2')

	# print(dloadlist)

	l = Lock()
	pool = Pool(initializer = init, initargs = (l,), processes = os.cpu_count())
	result = pool.map(dload, dloadlist)
	pool.close()
	pool.join()

# myfile = requests.get(url)
# open('F:/route views linx/rib.20131101.0000.bz2', 'wb').write(myfile.content)

# urllib.request.urlretrieve('http://archive.routeviews.org/route-views.linx/bgpdata/2013.11/RIBS/rib.20131101.0000.bz2', 'F:/route views linx/rib.20131101.0000.bz2')


# Download the file from `url` and save it locally under `file_name`:
# with urllib.request.urlopen(url) as response, open(file, 'wb') as out_file:
# 	data = response.read()  # a `bytes` object
# 	out_file.write(data)
