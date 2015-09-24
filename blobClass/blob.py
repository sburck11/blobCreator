### Blob

# pick starting pt on binary plot
# 
# Propagate:
	# get next pixel
	# check for hole on 1/0 plot using sweep line algo.
	# pick rand greater than blobThresh, less than surrounding blob +- innerThresh, color pixel

# fill outer:
	 pick random
	 

# 

class Blob():

	def __init__(self, numBlob, minSize, maxSize, outerThresh, blobThresh, innerThresh):
		self.binPlot=None
		self.lastPlot=None
		self.imgPlot=None
		self.numBlob=numBlob
		self.minSize=minSize
		self.maxSize=maxSize
		self.outerThresh=outerThresh
		self.blobThresh=blobThresh
		self.innerThresh=innerThresh
		self.lastPix=None

# Take coordinates of a pixel, return probability of pixel inclusion based on last pixels assigned.
	def getPix(self):
		if(self.lastPix=None):
			return #(random)
		neighbors=

	def pixProb(self, a, b):
		remProb = #random



00012
00002
00000
00000