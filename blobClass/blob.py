from PIL import Image
import numpy as np
import random

IMGSIZE = 10

class Blob():

	def __init__(self, numBlob, minSize, maxSize, outerThresh, blobThresh, innerThresh, sigma, dirPath, name):
		self.imgType=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		self.imgPlot=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		self.numBlob=numBlob
		self.minSize=minSize
		self.maxSize=maxSize
		self.outerThresh=outerThresh
		self.blobThresh=blobThresh
		self.innerThresh=innerThresh
		self.typeList=[]
		self.blobList=[]
		self.outerList=[]
		self.pix=None
		self.last=None
		# 0 = filling binType, 1 = filling blob, 2 = filling background
		self.stage=0
		#current blob being filles
		self.blobNum=0
		self.sigma=sigma
		self.dirPath=dirPath
		self.name=name



# Take coordinates of a pixel, return probability of pixel inclusion based on last pixels assigned.
	def getPix(self):
		if(self.pix==None):
			a=random.randint(0, (IMGSIZE-1))
			b=random.randint(0, (IMGSIZE-1))
			self.pix=(a, b)
			return
		if(self.stage==0):
			# print 'In getPix stg. 0'
			x=int(random.gauss(len(self.typeList), self.sigma))
			# print "Gaus: mu = " + str(len(self.typeList)) + ", sigma = " + str(self.sigma)
			# print "x = " + str(x)
			if(x>len(self.typeList)):
				x=len(self.typeList)-(x-len(self.typeList))
			x=x-1
			if(x<0):
				x=0
			# print 'Len typelist = ' + str(len(self.typeList))
			# print 'x=' + str(x)
			self.pix=self.typeList[x]
			self.typeList.remove(self.pix)
			return
		if(self.stage==1):
			x=int(random.gauss(len(self.blobList)/2, self.sigma))
			if(x>len(self.blobList)):
				x=len(self.blobList)-(x-len(self.blobList))
			x=x-1
			self.pix=self.blobList[x]
			blobList.pop([x])
			return
		if(self.stage==2):
			x=int(random.gauss(len(self.outerList)/2, self.sigma))
			if(x>len(self.outerList)):
				x=len(self.outerList)-(x-len(self.outerList))
			x=x-1
			self.pix=self.outerList[x]
			outerList.pop([x])
			return

	def checkNeighbors(self):
		pix=self.pix
		num=self.blobNum

		localRange=[-1, 0, 1]
		for i in localRange:
			if((i<0) or (i>(IMGSIZE-1))):
				break
			for j in localRange:
				if((j<0) or (j>(IMGSIZE-1))):
					break
				if(self.imgType[pix[0]+i][pix[1]+i]!=(num or 0)):
					return False
		return True


	def addNeighbors(self):
		neighborList=[]
		pix=self.pix

		if((pix[0]<(IMGSIZE-1)) and ((pix[0]+1, pix[1]) not in self.typeList)
			and (self.imgType[pix[0]+1, pix[1]]==0)):
				neighborList.append((pix[0]+1, pix[1]))
		if((pix[0]>0) and ((pix[0]-1, pix[1]) not in self.typeList)
			and (self.imgType[pix[0]-1, pix[1]]==0)):
				neighborList.append((pix[0]-1, pix[1]))
		if((pix[1]<(IMGSIZE-1)) and ((pix[0], pix[1]+1) not in self.typeList)
			and (self.imgType[pix[0], pix[1]+1]==0)):
				neighborList.append((pix[0], pix[1]+1))
		if((pix[1]>0) and ((pix[0], pix[1]-1) not in self.typeList)
			and (self.imgType[pix[0], pix[1]-1]==0)):
				neighborList.append((pix[0], pix[1]-1))

		if(random.randint(0, 1)==1):
			if((pix[0]<(IMGSIZE-1)) and (pix[1]<(IMGSIZE-1))
				and ((pix[0]+1, pix[1]+1) not in self.typeList) and (self.imgType[pix[0]+1, pix[1]+1]==0)):
				neighborList.append((pix[0]+1, pix[1]+1))
			if((pix[0]<(IMGSIZE-1)) and (pix[1]>0)
				and ((pix[0]+1, pix[1]-1) not in self.typeList) and (self.imgType[pix[0]+1, pix[1]-1]==0)):
				neighborList.append((pix[0]+1, pix[1]-1))
			if((pix[0]>0) and (pix[1]<(IMGSIZE-1))
				and ((pix[0]-1, pix[1]+1) not in self.typeList) and (self.imgType[pix[0]-1, pix[1]+1]==0)):
				neighborList.append((pix[0]-1, pix[1]+1))
			if((pix[0]>0) and (pix[1]>0)
				and ((pix[0]-1, pix[1]-1) not in self.typeList) and (self.imgType[pix[0]-1, pix[1]-1]==0)):
				neighborList.append((pix[0]-1, pix[1]-1))

		random.shuffle(neighborList)

		if(self.stage==0):
			self.typeList.extend(neighborList)
		if(self.stage==1):
			self.blobList.extend(neighborList)
		if(self.stage==2):
			self.outerList.extend(neighborList)
						
	def fillHoles(self, count, intervalList):
		closed=[]
		for j in range(IMGSIZE):
			rowIntervals=[]
			for i in range(IMGSIZE):
				for k in range(len(intervalList[i])):
					if(intervalList[i][k][0]<=j and intervalList[i][k][1]>=j):
						print 'Intersection at Col '+str(j)+', interval is '+str(intervalList[i][k])+' at row '+str(i)

	def holeSweep(self):
		print self.blobNum
		intervalList=[]
		for i in range(IMGSIZE):
			print "Sweeping Col: " + str(i)
			first=None
			last=None
			inBlob=False
			colIntervals=[]
			if(self.imgType[i,0]!=self.blobNum):
				# print 'NOPE!'
				first=0
			else:
				# print 'Blob starting at: '+str(0)
				inBlob=True
			for j in range(IMGSIZE):
				if(inBlob==True and self.imgType[i,j]!=self.blobNum):
					# print 'Blob ending at: '+str(j)
					inBlob=False
					first=j
				if(inBlob==False and (self.imgType[i,j]==self.blobNum or j==IMGSIZE-1)):
					# print 'Blob starting at: '+str(j)
					inBlob=True
					last=j-1
					if(j==IMGSIZE-1 or first==0):
						colIntervals.append((first, j, 'open', i))
					else:
						colIntervals.append((first, last, 'closed', i))
				# if(inBlob==False and j==IMGSIZE-1):
				# 	last=j-1
				# 	colIntervals.append((first, last, 'open'))
			intervalList.append(colIntervals)
			print colIntervals
		return intervalList
		# print intervalList

	def makeImg(self):
		img=Image.new('1', (IMGSIZE,IMGSIZE), 'black')
		self.imgType=img.load()

		for i in range(self.numBlob):
			self.blobNum=i+1
			# print 'WORKING ON PIX ' + str(i)
			blobSize = random.randint(self.minSize, self.maxSize)
			# print blobSize
			for i in range(blobSize):
				# print self.typeList
				self.last=self.pix
				self.getPix()
				# print self.pix
				# # print self.typeList
				# print '\n'
				if(self.checkNeighbors==False):
					goodPix=False
					while(goodPix==False):
						self.getPix()
						if(self.checkNeighbors==True):
							goodPix=True

				 # self.holeSweep()

				self.addNeighbors()
				# print "Pix = " + str(self.pix[0]) + ", " + str(self.pix[1])
				# print "pix val is " + str(self.imgType[self.pix[0], self.pix[1]])
				self.imgType[self.pix[0], self.pix[1]] = (1)
				# print i
				if(len(self.typeList)==0):
					print i

			#FILL SINGLE PIXEL HOLES!

			intervals=self.holeSweep()
			self.fillHoles(i, intervals)

			# if(self.fillHoles(intervals, i)==False):
			# 	GO BACK!!!
			print blobSize
		self.pix=None
		self.typeList=[]

		img.save(self.dirPath + '/' + self.name + '.png')




