from PIL import Image, ImageFilter
import numpy as np
import random
import math

IMGSIZE = 100

def mirrorDiag(plot):
	# print plot
	new=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
	for i in range(IMGSIZE):
		for j in range(IMGSIZE):

			new[i,j]=plot[j,i]
			new[j,i]=plot[i,j]
	# print new
	return new

class Blob():

	def __init__(self, numBlob, minSize, maxSize, blobThresh, innerThresh, sigma, shaderSigma, dirPath, betweenBlobs, touchingEdge, flatBG, filterOn, name):
		self.imgType=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		self.imgPlot=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		self.shaded=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
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
		# current blob being filles
		self.blobNum=0
		self.sigma=sigma
		self.shaderSigma=shaderSigma
		self.dirPath=dirPath
		self.name=name
		self.startPT=[]
		self.betweenBlobs=betweenBlobs
		self.touchingEdge=touchingEdge
		self.flatBG=flatBG
		self.filterOn=filterOn

	def clearSurrounding(self, x, y, rad, pixVal):
		# print 'in clearSurrounding x = '+str(x)+', y = '+str(y)
		for i in range(1+2*rad):
			a=i-rad
		# print i
			for j in range(1+2*rad):
				b=j-rad
			# print j
				if((0<=a+x<IMGSIZE) and (0<=b+y<IMGSIZE)):
					# print i, j
					if(self.imgType[a+x][b+y] not in pixVal):
						# print 'RETURNING FALSE'
						# print 'pixVal = '+str(pixVal)+', val at location = '+str(self.imgType[a+x, b+y])
					# print 'Returning false'
						return False
		return True

		

	def rootEdgeDist(self, size, pix):
		print size
		rad=math.sqrt(size/3.142)
		a=pix[0]
		b=IMGSIZE-1-pix[0]
		c=pix[0]
		d=IMGSIZE-1-pix[0]
		if(min(a,b,c,d)<(35)):#2*rad)):
			return False
		else:
			return True


# Take coordinates of a pixel, return probability of pixel inclusion based on last pixels assigned.
	def getPix(self,size):
		if(self.pix==None):
			if(self.touchingEdge==False):
				found=False
				while(found==False):
					a=random.randint(0, (IMGSIZE-1))
					b=random.randint(0, (IMGSIZE-1))
					if(self.clearSurrounding(a, b, self.betweenBlobs, [0])==True):
						# print 'true'
						# if(self.touchingEdge==True and self.rootEdgeDist(size, (a,b))==False):
						# 	continue
						self.pix=(a, b)
						found=True
						self.startPT.append(self.pix)
				return True
			else:
				a=random.randint(29,69)
				b=random.randint(29,69)
				self.pix=(a,b)
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
			# print self.typeList
			# print 'Len typelist = ' + str(len(self.typeList))
			# print 'x=' + str(x)+', i = '+str(i)+', size = '+str(size)
				return False
			self.pix=self.typeList[x]
			self.typeList.remove(self.pix)
			return True
		if(self.stage==1):
			if(len(self.blobList)==0):
				return False
		# print "In getPix stg 1"
		# print self.blobList
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

	def isEdge(self, pix):
		coords=[0,1,2,IMGSIZE-3,IMGSIZE-2,IMGSIZE-1]
		if(((pix[0] in coords) or (pix[1] in coords)) and self.touchingEdge==True):
			# print "IN COORDS!"
			return False
		else:
			return True

	def addNeighbors(self):
		neighborList=[]
		pix=self.pix
	# print 'In addNeighbors'
		if(self.stage==0):
			currentList=self.typeList
			pixType=0
		if(self.stage==1):
			currentList=self.blobList
			pixType=self.blobNum

		if(self.isEdge((pix[0]+1, pix[1])) and (pix[0]<(IMGSIZE-1)) and ((pix[0]+1, pix[1]) not in currentList)
			and (self.imgType[pix[0]+1, pix[1]]==pixType) and self.imgPlot[pix[0]+1, pix[1]]==0):
				neighborList.append((pix[0]+1, pix[1]))
		if(self.isEdge((pix[0]-1, pix[1])) and (pix[0]>0) and ((pix[0]-1, pix[1]) not in currentList)
			and (self.imgType[pix[0]-1, pix[1]]==pixType) and self.imgPlot[pix[0]-1, pix[1]]==0):
				neighborList.append((pix[0]-1, pix[1]))
		if(self.isEdge((pix[0], pix[1]+1)) and (pix[1]<(IMGSIZE-1)) and ((pix[0], pix[1]+1) not in currentList)
			and (self.imgType[pix[0], pix[1]+1]==pixType) and self.imgPlot[pix[0], pix[1]+1]==0):
				neighborList.append((pix[0], pix[1]+1))
		if(self.isEdge((pix[0], pix[1]-1)) and (pix[1]>0) and ((pix[0], pix[1]-1) not in currentList)
			and (self.imgType[pix[0], pix[1]-1]==pixType) and self.imgPlot[pix[0], pix[1]-1]==0):
				neighborList.append((pix[0], pix[1]-1))

		# if(self.stage==0):
		if((self.stage==0 and random.randint(0, 1)==1) or (self.blobNum==0)):
			if(self.isEdge((pix[0]+1, pix[1]+1)) and (pix[0]<(IMGSIZE-1)) and (pix[1]<(IMGSIZE-1)) and self.imgPlot[pix[0]+1, pix[1]+1]==0
				and ((pix[0]+1, pix[1]+1) not in currentList) and (self.imgType[pix[0]+1, pix[1]+1]==pixType)):
				neighborList.append((pix[0]+1, pix[1]+1))
			if(self.isEdge((pix[0]+1, pix[1]-1)) and (pix[0]<(IMGSIZE-1)) and (pix[1]>0) and self.imgPlot[pix[0]+1, pix[1]-1]==0
				and ((pix[0]+1, pix[1]-1) not in currentList) and (self.imgType[pix[0]+1, pix[1]-1]==pixType)):
				neighborList.append((pix[0]+1, pix[1]-1))
			if(self.isEdge((pix[0]-1, pix[1]+1)) and (pix[0]>0) and (pix[1]<(IMGSIZE-1)) and self.imgPlot[pix[0]-1, pix[1]+1]==0
				and ((pix[0]-1, pix[1]+1) not in currentList) and (self.imgType[pix[0]-1, pix[1]+1]==pixType)):
				neighborList.append((pix[0]-1, pix[1]+1))
			if(self.isEdge((pix[0]-1, pix[1]-1)) and (pix[0]>0) and (pix[1]>0) and self.imgPlot[pix[0]-1, pix[1]-1]==0
				and ((pix[0]-1, pix[1]-1) not in currentList) and (self.imgType[pix[0]-1, pix[1]-1]==pixType)):
				neighborList.append((pix[0]-1, pix[1]-1))

		random.shuffle(neighborList)

		if(self.stage==0):
			self.typeList.extend(neighborList)
		if(self.stage==1):
		# print "neighborList = " + str(neighborList)
			self.blobList.extend(neighborList)
		# print "blobList = " + str(self.blobList)
		if(self.stage==2):
			self.outerList.extend(neighborList)
						

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
				# print 'DUPES!'
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

	def getList(self, blobNum):
		center=[0.0,0.0]
		wWeight=[0]*IMGSIZE
		hWeight=[0]*IMGSIZE
		blobList=[]
		for i in range(IMGSIZE):
			for j in range(IMGSIZE):
				if(self.imgType[i,j]==blobNum):
					blobList.append((i,j))
					wWeight[i]=wWeight[i]+1
					hWeight[j]=hWeight[j]+1
		wPoint=0
		hPoint=0
		wBal=np.zeros((IMGSIZE), dtype=np.int)
		hBal=np.zeros((IMGSIZE), dtype=np.int)
		for i in range(IMGSIZE):
			# print 'i='+str(i)
			# Width balancing
			lWeight=0
			rWeight=0
			l=i-1
			r=i+1
			while(l>=0):
				lWeight=lWeight+wWeight[l]
				l=l-1
			while(r<IMGSIZE):
				# print 'r='+str(r)
				rWeight=rWeight+wWeight[r]
				r=r+1
			wBal[i]=abs(rWeight+lWeight)
			# Height balancing
			tWeight=0
			bWeight=0
			t=i-1
			b=i+1
			while(t>=0):
				tWeight=tWeight+hWeight[t]
				t=t-1
			while(b<IMGSIZE):
				bWeight=bWeight+hWeight[b]
				b=b+1
			hBal[i]=abs(tWeight+bWeight)
		wIndex=wBal.argmin()
		hIndex=hBal.argmin()
		blobList.sort(key=lambda x: abs(0-abs(x[0]-wIndex)-abs(x[1]-hIndex)))
		return blobList

	def getLegalShades(self):
		if(self.imgType[self.pix[0], self.pix[1]]==0):
			if(self.flatBG==True):
				shades=[1,1]
			else:
				shades=[1, 255-self.blobThresh]
		else:
			shades=[self.blobThresh+1, 255]
		# print 'FOR PIX '+str(self.pix)+':'+' Shades='+str(shades)
		seq=[-1, 0, 1]
		avgShade=[0, 0]
		for i in seq:
			a=self.pix[0]+i
			for j in seq:
				b=self.pix[1]+j
				# Don't check shade for selected pix, only for neighbors

				if(i==j==0):
					continue
				
				if((0<=a<IMGSIZE) and (0<=b<IMGSIZE)):
					# print 'Checking neighbor at: '+'('+str(a)+','+str(b)+')'

					# if(self.imgPlot[a,b]!=0):
						# print "Neighbor shade is: "+str(self.imgPlot[a,b])
					# If cell unshaded, skip
					if(self.imgPlot[a, b]==0):
						continue
					# Make sure blob thresh can be met by any border cells.
					if (self.imgType[a,b]==0 and shades[1]>255-self.blobThresh):
						shades[1]=255-self.blobThresh
					if (self.imgType[a,b]>0 and shades[0]<1+self.blobThresh):
						shades[0]=self.blobThresh+1

					# print 'before: ' + str(shades)
					if(self.imgType[a,b]!=self.imgType[self.pix[0], self.pix[1]] and self.imgPlot[a, b]!=0):
						# avgShade[0]=avgShade[0]+1
						# avgShade[1]=avgShade[1]+self.imgPlot[a, b]
						# print 'Not same type'
						if(self.imgType[a,b]==0):#In a blob next to non-blob
							if(shades[0]>(self.imgPlot[a,b]+self.blobThresh)):
								shades[0]=self.imgPlot[a,b]+self.blobThresh
								# print 'a ' + str(shades)
							# if(shades[1]>(self.imgPlot[a,b]-self.blobThresh)):
							# 	shades[1]=self.imgPlot[a,b]-self.blobThresh
						if(self.imgType[a,b]!=0):#In non-blob next to blob
							# if(shades[0]>(self.imgPlot[a,b]+self.blobThresh)):
							# 	shades[0]=self.imgPlot[a,b]+self.blobThresh
							if(shades[1]>(self.imgPlot[a,b]-self.blobThresh)):
								# print shades[1]
								# print self.blobThresh
								shades[1]=self.imgPlot[a,b]-self.blobThresh
								# print 'b ' + str(shades)
					if(self.imgType[a,b]==self.imgType[self.pix[0], self.pix[1]] and self.imgPlot[a, b]!=0):
						avgShade[0]=avgShade[0]+1
						avgShade[1]=avgShade[1]+self.imgPlot[a, b]
						# print 'Same type'
						if(shades[0]<(self.imgPlot[a,b]-self.innerThresh)):
							shades[0]=self.imgPlot[a,b]-self.innerThresh
							# print 'c ' + str(shades)
						if(shades[1]>(self.imgPlot[a,b]+self.innerThresh)):
							# print shades
							# print self.imgPlot[a, b]
							shades[1]=self.imgPlot[a,b]+self.innerThresh
							# print 'd ' + str(shades)
					# print 'Final shades is: '+str(shades)+'\n'
		# print 'Shades = ' + str(shades)
		if(shades[0]>shades[1]):
					x=(shades[0]+shades[1])/2
					shades[0]=x
					shades[1]=x
		if(avgShade[0]!=0):
			avgShade=avgShade[1]/avgShade[0]
		else:
			avgShade=random.randint(shades[0], shades[1])
		# print avgShade
		return (shades[0], shades[1]), avgShade
					
	def fillShades(self):
		## ITERATE BY ROW+COL

		# for i in range(IMGSIZE):
		# 	for j in range(IMGSIZE):
		# 		self.pix=(i, j)
		# 		shades, avgShade=self.getLegalShades()
		# 		avgShade=np.clip([avgShade], shades[0], shades[1])
		# 		avgShade=avgShade[0]
		# 		if(shades[0]>shades[1]):
		# 			x=(shades[0]+shades[1])/2
		# 		else:
		# 			# print shades
		# 			sig=int(float(self.shaderSigma)/100*(shades[1]-shades[0]))
		# 			# print avgShade
		# 			# print sig
		# 			# print shades[1]-shades[0]
		# 			# print 'HERE: '+str(float(self.shaderSigma)/100)
		# 			# print self.shaderSigma
		# 			x=int(random.gauss(avgShade, sig))
		# 			# x=x+shades[0]
		# 			if(x>shades[1]):
		# 				x=shades[1]-(x-shades[1])
		# 			if(x<shades[0]):
		# 				x=shades[0]
		# 			# x=random.randint(shades[0], shades[1])
		# 		self.imgPlot[self.pix[0], self.pix[1]]=x

		## ITERATE RANDOMLY

		# cells=[]
		# for i in range(IMGSIZE):
		# 	for j in range(IMGSIZE):
		# 		cells.append((i, j))
		# random.shuffle(cells)
		# for i in range(len(cells)):
		# 	# print i
		# 	# print len(cells)
		# 	self.pix=cells.pop()
		# 	shades, avgShade=self.getLegalShades()
		# 	# print "First: "
		# 	# print avgShade
		# 	avgShade=np.clip([avgShade], shades[0], shades[1])
		# 	avgShade=avgShade[0]
		# 	# print avgShade
		# 	if(shades[0]>shades[1]):
		# 		x=(shades[0]+shades[1])/2
		# 	else:
		# 		# avgShade=np.clip
		# 		x=int(random.gauss(int(avgShade), self.shaderSigma))
		# 		# print x
		# 		if(x>shades[1]):
		# 			x=shades[1]-(x-shades[1])
		# 		if(x<shades[0]):
		# 			x=shades[0]
		# 			# x=random.randint(shades[0], shades[1])
		# 	self.imgPlot[self.pix[0], self.pix[1]]=x
			# currently all blobs black
			# 0=white 255=black

		## Iterate pix from center
		for i in range(self.numBlob+1):
			# i=self.numBlob-i
			pixList=self.getList(i)
			for j in pixList:
				# print 'blob '+str(i)+'pix '+str(j)
				self.pix=j
				shades, avgShade=self.getLegalShades()
				avgShade=np.clip([avgShade], shades[0], shades[1])
				avgShade=avgShade[0]
				# if(shades[0]>shades[1]):
				# 	x=(shades[0]+shades[1])/2
				# else:
					# print shades
				sig=int(float(self.shaderSigma)/100*(shades[1]-shades[0]))
				# print avgShade
				# print sig
				# print shades[1]-shades[0]
				# print 'HERE: '+str(float(self.shaderSigma)/100)
				# print 'shaderSigma='+str(sig)
				x=int(random.gauss(avgShade, sig))
				# x=x+shades[0]
				if(x>shades[1]):
					x=shades[1]-(x-shades[1])
				if(x<shades[0]):
					x=shades[0]
					# x=random.randint(shades[0], shades[1])
				self.imgPlot[self.pix[0], self.pix[1]]=x



	def makeImg(self):
		img=Image.new('RGB', (IMGSIZE,IMGSIZE), 'white')
		# self.imgType=img.load()
		print 'Making image: '+self.name

		for i in range(self.numBlob):
			# print "\n\n\n\n\nblob: " + str(i)
			self.blobNum=i+1
			# print 'In Make Img, WORKING ON PIX ' + str(i)

			blobSize = random.randint(self.minSize, self.maxSize)
			# print blobSize
			for j in range(blobSize):
				self.last=self.pix
				if(self.getPix(blobSize)==False):
					break
				legalPix=[0, self.blobNum]
				if(j==0):
					if(self.clearSurrounding(self.pix[0], self.pix[1], IMGSIZE*(1/3), legalPix)==False):
						goodPix=False
						while(goodPix==False):
							if(self.getPix(blobSize)==False):
								break
							if(self.clearSurrounding(self.pix[0], self.pix[1], IMGSIZE*(1/3), legalPix)==True):
								goodPix=True
				else:
					if(self.clearSurrounding(self.pix[0], self.pix[1], self.betweenBlobs, legalPix)==False):
						goodPix=False
						while(goodPix==False):
							if(self.getPix(blobSize)==False):
								break
							if(self.clearSurrounding(self.pix[0], self.pix[1], self.betweenBlobs, legalPix)==True):
								goodPix=True

				self.addNeighbors()
				# print "Pix = " + str(self.pix[0]) + ", " + str(self.pix[1])
				# print "pix val is " + str(self.imgType[self.pix[0], self.pix[1]])
				self.imgType[self.pix[0], self.pix[1]] = self.blobNum
				# print i
				# if(len(self.typeList)==0):
					# print i

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

		self.fillShades()

		toSave=img.load()

		for i in range(IMGSIZE):
			for j in range(IMGSIZE):
				toSave[i,j]=(self.imgPlot[i,j],0,255-self.imgPlot[i,j])#255-self.imgPlot[i,j]

		self.pix=None
		# self.typeList=[]
		# img.save(self.dirPath + '/' + 'BEFORE_FILTER_'+self.name + '.png')
		if(self.filterOn==True):
			img=img.filter(ImageFilter.BLUR)
		img.save(self.dirPath + '/' + self.name + '.png')



		#bimg=Image.new('1', (IMGSIZE, IMGSIZE), 'black')
		# bToSave=bimg.load()
		# for i in range(IMGSIZE):
		# 	for j in range(IMGSIZE):
		# 		if(self.imgType[i, j]==0):
		# 			bToSave[i, j]=1
		# 		else:
		# 			bToSave[i, j]=0
		# bimg.save(self.dirPath + '/BW.png')

		# self.imgPlot=mirrorDiag(self.imgPlot)
		# self.imgType=mirrorDiag(self.imgType)

		# print self.imgType
		# print self.imgPlot

