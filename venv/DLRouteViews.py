import urllib.request, urllib.error
from multiprocessing import Pool
import os  # file műveletek
import datetime
from datetime import date

ix = ['jinx', 'linx', 'sydney', 'eqix']  # linx  sydney  jinx  eqix

# url = 'http://archive.routeviews.org/route-views.linx/bgpdata/2013.11/RIBS/rib.20131101.0000.bz2'
# file = 'F:/route views linx/rib.20131101.0000.bz2'
# C:/teszt/DL_teszt/rib_    /mnt/rib_
file_root_loc = '/mnt/rib_'
dloadlist = []
mo = ''
da = ''


def log_dl_err(loc, error, filename):
	with open(loc + 'error.txt', 'a+') as f:
		time = datetime.datetime.now()
		f.write(error + '\t' + filename + '\t' + str(time) + '\t' + '\n')
		f.close()


def dload(url):
	proc = os.getpid()
	start_time = datetime.datetime.now()
	print('{0}  by process id: {1} at: {2}'.format(url, proc, start_time))

	file_name = url.split('/')[7]
	current_ix = url.split('/')[3].split('.')[1]
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
						print(str(y) + ' ' + str(mo) + ' ' + str(da))
						for i in ix:
							dloadlist.append('http://archive.routeviews.org/route-views.' + i + '/bgpdata/201' + str(y) + '.' + str(mo) + '/RIBS/rib.201' + str(y) + str(mo) + str(da) + '.0000.bz2')
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
							dloadlist.append('http://archive.routeviews.org/route-views.' + i + '/bgpdata/201' + str(y) + '.' + str(mo) + '/RIBS/rib.201' + str(y) + str(mo) + str(da) + '.0000.bz2')
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
							dloadlist.append('http://archive.routeviews.org/route-views.' + i + '/bgpdata/201' + str(y) + '.' + str(mo) + '/RIBS/rib.201' + str(y) + str(mo) + str(da) + '.0000.bz2')

	# print(dloadlist[2].split('/')[7])

	pool = Pool(processes = os.cpu_count())
	result = pool.map(dload, dloadlist)

# myfile = requests.get(url)
# open('F:/route views linx/rib.20131101.0000.bz2', 'wb').write(myfile.content)

# urllib.request.urlretrieve('http://archive.routeviews.org/route-views.linx/bgpdata/2013.11/RIBS/rib.20131101.0000.bz2', 'F:/route views linx/rib.20131101.0000.bz2')


# Download the file from `url` and save it locally under `file_name`:
# with urllib.request.urlopen(url) as response, open(file, 'wb') as out_file:
# 	data = response.read()  # a `bytes` object
# 	out_file.write(data)
