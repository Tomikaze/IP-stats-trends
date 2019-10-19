
ix = ['jinx', 'linx', 'sydney', 'eqix']  # linx  sydney  jinx  eqix


url = 'http://archive.routeviews.org/route-views.linx/bgpdata/2013.11/RIBS/rib.20131101.0000.bz2'

print( url.split('/')[3].split('.')[1])



for i in ix:
	print('http://archive.routeviews.org/route-views.' + i + '/bgpdata/201' + '/RIBS/rib.201' +'.0000.bz2')