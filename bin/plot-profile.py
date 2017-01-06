#!/usr/bin/env python
# a bar plot with errorbars
import numpy as npy
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from pylab import std, mean

#import gtk
from matplotlib.mlab import csv2rec, rec2csv
#, rec2gtk

import sys

datafile = sys.argv[1]
output_basename = sys.argv[2]
try:
    r = csv2rec(datafile, checkrows=0)
except Exception, err:
    raise Exception("Unable to parse CSV: %s: %s" %( datafile, err ))

data = dict(
    stdlib=dict(),
    uriref=dict(),
    urlparse=dict())

r.sort()

for l in r:
    l = list(l)
    lib, tests, iterations = l[:3]
    #if iterations not in data[lib]:
    #    data[lib][iterations] = {}
    data[lib][iterations] = l[3:]


stdPairs = [[],[]]
dataPairs = [[],[]]
groups = data['stdlib'].keys()
groups.sort()
for iterations in groups:
	urlparse_times = data['stdlib'][iterations]
	uriref_times = data['uriref'][iterations]

	dataPairs[0].append(mean(uriref_times)/iterations)
	dataPairs[1].append(mean(urlparse_times)/iterations)
	stdPairs[0].append(std(uriref_times)/iterations)
	stdPairs[1].append(std(urlparse_times)/iterations)

#for x,y in pairs:
#    print 'mean=%1.2f, std=%1.2f, r=%1.2f'%(mean(y), std(y),
#            corrcoef(x,y)[0][1])

#scroll = rec2gtk(r, formatd=formatd)
#
#win = gtk.Window()
#win.set_size_request(600,800)
#win.add(scroll)
#win.show_all()
#gtk.main()
#

N = len(groups)

urirefMeans = dataPairs[1]
urirefStd = stdPairs[1]


ind = npy.arange(N)  # the x locations for the groups
width = 0.35       # the width of the bars

fig = plt.figure()
ax = fig.add_subplot(111)
#print ind, urirefMeans
rects1 = ax.bar(ind, urirefMeans, width, color='#ad7fa8', yerr=urirefStd)


urlparseMeans = dataPairs[0]
urlparseStd = stdPairs[0]
rects2 = ax.bar(ind+width, urlparseMeans, width, color='#fcaf3e', yerr=urlparseStd)

#a = [ pow(10,i) for i in range(10) ]




# add some
ax.set_ylabel('Seconds')
ax.set_title('Time by iterations')
ax.set_xticks(ind+width)
ax.set_xticklabels( groups )

ax.legend(
    (rects1[0], rects2[0]),
    ( 'stdlib','uriref',) )

def autolabel(rects):
    # attach some text labels
    for rect in rects:
        height = rect.get_height()
        ax.text(rect.get_x()+rect.get_width()/2., 1.05*height, '%d'%int(height),
                ha='center', va='bottom')

#autolabel(rects1)
#autolabel(rects2)


#plt.ylim(0.001, 100)
#ax.set_yscale('log')
#plt.ylim(0.001, 1000)
#plt.show()
plt.savefig(output_basename+'.png', format='png')
plt.savefig(output_basename+'.svg', format='svg')

