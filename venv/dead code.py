def moreSpecPref_v1():  # első prefix tárolása default gatewayel

	print('msp start ')
	print(datetime.datetime.now())

	# storeList.sort(key = operator.attrgetter('prefix'))
	cnt = 0
	for hasito in storeList:

		if ( not hasito.prefix=='24'):
			for hasitott in storeList[cnt:]:
				if (not hasito.bin[0:8] == hasitott.bin[0:8]):
					break
				if (hasito.prefix < hasitott.prefix):
					if( hasito.bin[0:int(hasito.prefix)] == hasitott.bin[0:int(hasito.prefix)]):
						prefixCount[int(hasito.prefix)]+=1
						# print(str(cnt-1)+':'+str(hasito.address))


		cnt += 1
		# print(*prefixCount)
		if (cnt%50000==0):
			print(str(cnt - 1) + ':' + str(hasito.address))

