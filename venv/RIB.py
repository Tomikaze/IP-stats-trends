import os
import datetime

# cd /mnt/c/users/bakit/PycharmProjects/IP-stats-trends/venv
# cd /mnt/c/teszt/t
# https://manpages.debian.org/testing/bgpdump/bgpdump.1.en.html
# bgpdump rib.20190101.0000.bz2 -O 20190101.txt

location ='/mnt/c/teszt/t/'
file= 'rib.20190101.0000.bz2'

myCmd= 'bgpdump '+location+file+ ' -O '+ location+ '20190101.txt'
print(myCmd)
os.system(myCmd)
print(datetime.datetime.now())
