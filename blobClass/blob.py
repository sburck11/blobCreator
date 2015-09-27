from PIL import Image
import numpy as np
import random
### Blob

# typePlot:
# 	get random point
# 	pick random point with probability of being close to last picked
# 	Keep a list of neighboring points, most recently added pushed at end.

# Implement hole checking algo later

# imgPlot:
# 	for blob:
# 		Pick random blob pt.
# 		pick random color #
# 		add neighboring points to array
# 		pick pt from array based on distribution
# 		add neighbors to array
# 		pick color based on distribution

# 	for bg:
# 		pick random point
# 		add neighbors
# 		get neighbor color

# getNeighbors:
# 	return list of neighboring cells

# getNeighbor color:
# 	return color of neighbor with prob dist. based on darkest/lightest

# get max color:
# 	get color limit based on dist. to blob and max thresh


class Blob():

	def __init__(self, numBlob, minSize, maxSize, outerThresh, blobThresh, innerThresh):
		self.binType=np.zeros((100, 100), dtype = numpy.int)
		self.imgPlot=np.zeros((100, 100), dtype = numpy.int)
		self.numBlob=numBlob
		self.minSize=minSize
		self.maxSize=maxSize
		self.outerThresh=outerThresh
		self.blobThresh=blobThresh
		self.innerThresh=innerThresh
		self.outerPixList=None
		self.innerPixList=None
		self.pix=None
		# 0 = filling binType, 1 = filling blob, 2 = filling background
		self.stage=0



# Take coordinates of a pixel, return probability of pixel inclusion based on last pixels assigned.
	def getPix(self):
		if(self.pix=None):
			a=random.randint(0, 255)
			b=random.randint(0, 255)
			self.typePlot[a][b]=2
			self.pix=(a, b)
			return (a, b)
		if(self.stage=True)
			x=random.gauss(0, len(self.))


	def pixProb(self, a, b):
		remProb = #random



00012
00002
00000
00000