# We read the CCA data generated by Taylor's CCA code
# and cluster the regions 
# and label each region

import scipy.io
import heapq


numberOfClusters = 6
numberOfWordsForEachCloud = 10
mat = scipy.io.loadmat('opinion_space_live2.mat')

Zcca = mat['Zcca']
Comments = mat['CommentMap']
Y = mat['Y']
featureMap=mat['FeatureMap']
print featureMap.shape
for i in featureMap:
	print i
print 'featuremap ended-----------------------'
# print type(Zcca) 
# The type of Zcca is numpy.ndarray
print Zcca.shape # (5, 1826)
print Zcca[:,0].shape #Be carefull in scipy indices start from 0
print Zcca[:,0]
print Comments.shape

"""
make a scatter plot with varying color and size arguments
http://matplotlib.sourceforge.net/examples/pylab_examples/scatter_demo2.html
"""
import matplotlib
from numpy import empty

import matplotlib.pyplot as plt


dotsize = empty(Comments.shape[1])
print 'Dot siz= ', dotsize.shape
print type(Comments)
print 'Comments.shape',Comments.shape

j=0
for i in Comments[0,:]:
	#print i, ': ', i[0].shape, ' Type=',type(i[0]), ' lenght=', len(i[0]), '\n\n\n'
	dotsize[j]=len(i[0])
	j=j+1

dotsizeNormalized =dotsize/dotsize.max()
print 'Max of dotsize = ', dotsize.max()
print 'Min of dotsize = ', dotsize.min()
import numpy
from scipy.cluster.vq import *

# let scipy do its magic (k==3 groups)
res, idx = kmeans2(numpy.array(zip(Zcca[0,:], Zcca[1,:])),numberOfClusters)
print '----------Residuals---------------'
print res
# convert groups to rbg 3-tuples.
colors = ([([0,0,0],[1,0,0],[0,0,1],[1,1,0],[0,1,1],[1,0,1])[i] for i in idx])

fig = plt.figure()
ax = fig.add_subplot(111)
ax.scatter(Zcca[0,:], Zcca[1,:], s=dotsizeNormalized*200, c=colors, marker='o', cmap=None, norm=None,
        vmin=None, vmax=None, alpha=0.35, linewidths=None,
        verts=None)
   
print '---------------'
print res[:,0]
print '---------------'
print res[:,1]     
print '-----------------shapes------------'
print res[:,0].shape
print '-'
print res[:,1].shape
print '----------------------------------'
x = res[:,0]
y = res[:,1]
ax.scatter(x,y, s=300, c='b',marker='d')

ax.set_xlabel(r'$\Delta_i$', fontsize=20)
ax.set_ylabel(r'$\Delta_{i+1}$', fontsize=20)
ax.set_title('CCA Visualization')
ax.grid(True)

from numpy import zeros
print Y.shape
print Y.shape[0]
numz=  Y.shape[0]
print type(numz),'type of numz'
print type(numberOfClusters), 'type of number of clusters'
myClusters = zeros((numz,numberOfClusters))
print myClusters.shape
clusterA= ((idx ==1))
print clusterA
for i in range(0,1825):
	for j in range(0,numz):
		myClusters[j,idx[i]]=myClusters[j,idx[i]]+Y[j,i]
	
from numpy import save, savetxt
from numpy import nonzero
#save('data.csv', myClusters, fmt='%.6f', delimiter=';')
savetxt("myfile.txt", myClusters)
texts = ['' for i in range(0, numberOfClusters)]
for i in range(0,numberOfClusters):
	mymax=myClusters[:,i].max()
	print 'Cluster = ', i, 'max=', mymax
	print 'Type of myClusters = ', type(myClusters[:,i].tolist())
	mylist=myClusters[:,i].tolist()
	elements = heapq.nlargest(numberOfWordsForEachCloud, mylist)
	print elements
	mydex=nonzero(myClusters[:,i]==myClusters[:,i].max())[0][0]
	mytopwordsindex = nonzero(myClusters[:,i]>=min(elements))
	print 'the index for the word is:', mydex
	#print 'size of mytopwordsindex is:', mytopwordsindex.shape
	print 'the index for the words is:', mytopwordsindex
	print 'actual word:', featureMap[0,mydex]
	print 'actual words are:', featureMap[0,mytopwordsindex]
	mywords = featureMap[0,mytopwordsindex][0].tolist()
	textotxy =' '
	print 'My words =', mywords
	#myfinalwords = textotxy.join(mywords.tolist())
	for l in range(0, numberOfWordsForEachCloud):
		
		textotxy = textotxy + '\n '+ mywords[l][0].capitalize()
		print textotxy
		a= mywords[l]
		print a[0]
	#texts[i] = featureMap[0,mydex][0].capitalize()
	texts[i] = textotxy
	



for i in range(0,len(x)):
	plt.annotate(texts[i], (x[i],y[i]), xytext=None, bbox=dict(boxstyle="round", fc="0.8"),size=10, va="center")
	#plt.annotate(texts[i], (x[i],y[i]), xytext=None, bbox=dict(boxstyle="round", fc="0.8"),size=20, va="center")
	
ax.scatter(x,y, s=300, c='b',marker='d')
plt.savefig("pyplot_text.png") 
plt.show()
