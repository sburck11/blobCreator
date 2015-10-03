from PIL import Image
import numpy as np
import random

IMGSIZE = 100

class Blob():

	def __init__(self, numBlob, minSize, maxSize, blobThresh, innerThresh, sigma, dirPath, name):
		self.imgType=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		self.imgPlot=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		self.numBlob=numBlob
		self.minSize=minSize
		self.maxSize=maxSize
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
		self.startPT=[]

	def clearSurrounding(self, x, y, rad, pixVal):
		# print 'in clearSurrounding x = '+str(x)+', y = '+str(y)
		for i in range(1+2*rad):
			a=i-rad
			for j in range(1+2*rad):
				b=j-rad
				if((0<=a+x<IMGSIZE) and (0<=b+y<IMGSIZE)):
					# print i, j
					if(self.imgType[a+x][b+y] not in pixVal):
						# print 'RETURNING FALSE'
						# print 'pixVal = '+str(pixVal)+', val at location = '+str(self.imgType[a+x, b+y])
						return False
		return True

# Take coordinates of a pixel, return probability of pixel inclusion based on last pixels assigned.
	def getPix(self,i ,size):
		if(self.pix==None):
			found=False
			while(found==False):
				a=random.randint(0, (IMGSIZE-1))
				b=random.randint(0, (IMGSIZE-1))
				if(self.clearSurrounding(a, b, 5, [0])==True):
					# print 'true'
					self.pix=(a, b)
					found=True
					self.startPT.append(self.pix)
			return True
		if(self.stage==0):
			# print 'In getPix stg. 0'

			localSigma=len(self.typeList)*(self.sigma/50)
			x=int(random.gauss(len(self.typeList), localSigma))
			# print "Gaus: mu = " + str(len(self.typeList)) + ", sigma = " + str(self.sigma)
			# print "x = " + str(x)
			if(x>len(self.typeList)):
				x=len(self.typeList)-(x-len(self.typeList))
			x=x-1
			if(x<0):
				x=0
			if(len(self.typeList)==0):
				print self.typeList
				print 'Len typelist = ' + str(len(self.typeList))
				print 'x=' + str(x)+', i = '+str(i)+', size = '+str(size)
				return False
			self.pix=self.typeList[x]
			self.typeList.remove(self.pix)
			return True
		if(self.stage==1):
			localSigma=len(self.blobList)*(self.sigma/50)
			x=int(random.gauss(len(self.blobList)/2, localSigma))
			if(x>len(self.blobList)):
				x=len(self.blobList)-(x-len(self.blobList))
			x=x-1
			self.pix=self.blobList.pop()

			return True
		# if(self.stage==2):
		# 	localSigma=len(self.blobList)*(self.sigma/50)
		# 	x=int(random.gauss(len(self.outerList)/2, localSigma))
		# 	if(x>len(self.outerList)):
		# 		x=len(self.outerList)-(x-len(self.outerList))
		# 	x=x-1
		# 	self.pix=self.outerList[x]
		# 	outerList.pop([x])
		# 	return True

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
						
	# def fillHoles(self, count, intervalList):
	# 	closed=[]
	# 	for j in range(IMGSIZE):
	# 		rowIntervals=[]
	# 		for i in range(IMGSIZE):
	# 			for k in range(len(intervalList[i])):
	# 				if(intervalList[i][k][0]<=j and intervalList[i][k][1]>=j):
	# 					print 'Intersection at Row '+str(j)+', interval is '+str(intervalList[i][k])+' at Col '+str(i)

	# def holeSweep(self):
	# 	print self.blobNum
	# 	intervalList=[]
	# 	for i in range(IMGSIZE):
	# 		print "Sweeping Col: " + str(i)
	# 		first=None
	# 		last=None
	# 		inBlob=False
	# 		colIntervals=[]
	# 		if(self.imgType[i,0]!=self.blobNum):
	# 			# print 'NOPE!'
	# 			first=0
	# 		else:
	# 			# print 'Blob starting at: '+str(0)
	# 			inBlob=True
	# 		for j in range(IMGSIZE):
	# 			if(inBlob==True and self.imgType[i,j]!=self.blobNum):
	# 				# print 'Blob ending at: '+str(j)
	# 				inBlob=False
	# 				first=j
	# 				# if(j==IMGSIZE-1):
	# 				# 	colIntervals.append((IMGSIZE-1, IMGSIZE-1, 'open', i))
	# 			if(inBlob==False and (self.imgType[i,j]==self.blobNum or j==IMGSIZE-1)):
	# 				# print 'Blob starting at: '+str(j)
	# 				inBlob=True
	# 				last=j-1
	# 				if(j==IMGSIZE-1 or first==0):
	# 					colIntervals.append((first, j, 'open', i))
	# 				else:
	# 					colIntervals.append((first, last, 'closed', i))
	# 			# if(inBlob==False and j==IMGSIZE-1):
	# 			# 	last=j-1
	# 			# 	colIntervals.append((first, last, 'open'))
	# 		intervalList.append(colIntervals)
	# 		print colIntervals
	# 	return intervalList
		# print intervalList

	def holeBFS(self):
		vertices=[]
		for i in range(2):
			x=i*(IMGSIZE-1)
			for j in range(IMGSIZE):
				if(self.imgType[x, j]!=self.blobNum):
					vertices.append((x, j))
		for i in range(2):
			if(i==1):
				x=i*(IMGSIZE-1)
			else:
				x=0
			for j in range(IMGSIZE-2):
				if(self.imgType[j+1, x]!=self.blobNum):
					vertices.append((j+1, x))
		visited=[[0] * IMGSIZE for i in range(IMGSIZE)]
		count=0
		while(len(vertices)!=0):
			# print vertices
			i=vertices.pop(0)
			# if(i in vertices):
			# 	print 'DUPES!'
			# print i
			# print vertices
			# print '\n'
			# print i, i[0], i[1]
			# print visited[i[0]][i[1]]
			# print i
			if(visited[i[0]][i[1]]!=1):
				visited[i[0]][i[1]]=1
				if((i[0]-1)>0 and self.imgType[i[0]-1,i[1]]!=self.blobNum):
					if (i[0]-1,i[1]) not in vertices:
						vertices.append((i[0]-1, i[1]))
				if((i[0]+1)<(IMGSIZE-1) and self.imgType[i[0]+1,i[1]]!=self.blobNum):
					if (i[0]+1,i[1]) not in vertices:
						vertices.append((i[0]+1, i[1]))
				if((i[1]-1)>0 and self.imgType[i[0],i[1]-1]!=self.blobNum):
					if (i[0],i[1]-1) not in vertices:
						vertices.append((i[0], i[1]-1))
				if((i[1]+1)<(IMGSIZE-1) and self.imgType[i[0],i[1]+1]!=self.blobNum):
					if (i[0],i[1]+1) not in vertices:
						vertices.append((i[0], i[1]+1))
		return visited

	def fillHoleBFS(self, visited):
		toFill=[]
		for i in range(IMGSIZE):
			for j in range(IMGSIZE):
				if(visited[i][j]!=1 and self.imgType[i,j]==0):
					toFill.append((i,j))
		return toFill

	def findBGPix(self):
		for i in range(IMGSIZE):
			for j in range(IMGSIZE):
				if(self.imgType[i,j]==0):
					self.pix=(i,j)
					return

	def getLegalShades(self):
		shades=(1,255)
		seq=[-1, 0, 1]
		for i in seq:
			a=self.pix[0]+i
			for j in seq:
				b=self.pix[1]+j
				# Don't check shade for selected pix, only for neighbors
				if(i==j==0):
					continue
				if((0<=a<IMGSIZE) and (0<=b<IMGSIZE)):
					# If cell unshaded, skip
					if(self.imgPlot[a, b]==0):
						continue
					# Make sure blob thresh can be met by any border cells.
					if (self.imgType[a,b]==0 and shades[1]>255-self.blobThresh):
						shades[1]=255-self.blobThresh
					if (self.imgType[a,b]!=0 and shades[0]<1+self.blobThresh):
						shades[0]=1+self.blobThresh

					if(self.imgType[a,b]!=self.imgType[self.pix[0], self.pix(1)]):
						if(self.imgType[a,b]==0):
							if(shades[0]<(self.imgPlot[a,b]-self.blobThresh)):
								shades[0]=self.imgPlot[a,b]-self.blobThresh
							if(shades[1]>(self.imgPlot[a,b]-self.blobThresh)):
								shades[1]=self.imgPlot[a,b]-self.blobThresh
						if(self.imgType[a,b]!=0):
							if(shades[0]>(self.imgPlot[a,b]+self.blobThresh)):
								shades[0]=self.imgPlot[a,b]+self.blobThresh
							if(shades[1]<(self.imgPlot[a,b]+self.blobThresh)):
								shades[1]=self.imgPlot[a,b]+self.blobThresh
					else:
							if(shades[0]<(self.imgPlot[a,b]-self.innerThresh)):
								shades[0]=self.imgPlot[a,b]-self.innerThresh
							if(shades[1]>(self.imgPlot[a,b]-self.innerThresh)):
								shades[1]=self.imgPlot[a,b]-self.innerThresh
		print shades
		return shades
					


	def fillShades(self, i):

		filled=False

		while(filled==False):
			if(self.pix==None):
				if(i==0)
					self.findBGPix()
				else:
					self.pix=self.startPT.pop()
			else:
				if(self.getPix()==False):
					filled=True
					continue
			self.addNeighbors()
			shades=self.getLegalShades()
			print shades
			# if(shades==None):

			x=int(random.gauss((shades[1]*2), self.sigma))
			if(x>shades[1]):
				x=shades[1]
			if(x<shades[0]):
				x=shades[0]
			self.imgPlot[self.pix[0], self.pix[1]]=x



	def makeImg(self):
		img=Image.new('L', (IMGSIZE,IMGSIZE), 'black')
		# self.imgType=img.load()

		for i in range(self.numBlob):
			# print "\n\n\n\n\nblob: " + str(i)
			self.blobNum=i+1
			# print 'WORKING ON PIX ' + str(i)
			blobSize = random.randint(self.minSize, self.maxSize)
			# print blobSize
			for j in range(blobSize):

				self.last=self.pix
				if(self.getPix(j, blobSize)==False):
					break
				legalPix=[0, self.blobNum]
				if(self.clearSurrounding(self.pix[0], self.pix[1], 5, legalPix)==False):
					goodPix=False
					while(goodPix==False):
						if(self.getPix(j, blobSize)==False):
							break
							break

						if(self.clearSurrounding(self.pix[0], self.pix[1], 5, legalPix)==True):
							goodPix=True

				self.addNeighbors()
				# print "Pix = " + str(self.pix[0]) + ", " + str(self.pix[1])
				# print "pix val is " + str(self.imgType[self.pix[0], self.pix[1]])
				self.imgType[self.pix[0], self.pix[1]] = self.blobNum
				# print i
				# if(len(self.typeList)==0):
				# 	print i

				if((j==(blobSize/2)) or (j==(3*blobSize/4)) or j==blobSize-1):

					visited=self.holeBFS()
					toFill=self.fillHoleBFS(visited)
					j=j-len(toFill)
					# print toFill
					for k in toFill:
						self.imgType[k[0],k[1]]=self.blobNum
					# print 'FILLED '+str(len(toFill))+' PIX'

			self.pix=None
			self.typeList=[]
		self.stage=1
		for i in range(self.numBlob+1):
			if(i==0):
				self.findBGPix()
				self.fillShades(i)

			else:
				self.fillShades(i)

		toSave=img.load()
		# for i in range(IMGSIZE):
		# 	for j in range(IMGSIZE):
		# 		if(self.imgType[i,j]==0):
		# 			toSave[i,j]=0
		# 		if(self.imgType[i,j]==1):
		# 			toSave[i,j]=75
		# 		if(self.imgType[i,j]==2):
		# 			toSave[i,j]=160
		# 		if(self.imgType[i,j]==3):
		# 			toSave[i,j]=255

		for i in range(IMGSIZE):
			for j in range(IMGSIZE):
				toSave[i,j]=self.imgPlot[i,j]

		self.pix=None
		# self.typeList=[]

		img.save(self.dirPath + '/' + self.name + '.png')




