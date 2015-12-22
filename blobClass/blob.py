from PIL import Image, ImageFilter
import numpy as np
import random
import math

IMGSIZE = 100

# Used for debugging
def mirrorDiag(plot):
	new=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
	for i in range(IMGSIZE):
		for j in range(IMGSIZE):
			new[i,j]=plot[j,i]
			new[j,i]=plot[i,j]
	return new

class Blob():

	def __init__(self, numBlob, minSize, maxSize, blobThresh, innerThresh, sigma, shaderSigma, dirPath, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name):
		# 0 if background pixel, else pixel represents which blob (1 for blob 1, 2 for blob 2 etc).
		self.imgType=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		# Holds val 0-255 for color intensity, 0=blue 255=red.
		self.imgPlot=np.zeros((IMGSIZE, IMGSIZE), dtype=np.int)
		# Number of blobs in image.
		self.numBlob=numBlob
		# Minimum and maximum permitted blob sizes.
		self.minSize=minSize
		self.maxSize=maxSize
		# Minimum color difference between neighboring blob and background pixels, 0-255.
		self.blobThresh=blobThresh
		# Maximum difference between neighboring pixels within a blob or background.
		self.innerThresh=innerThresh
		# Used to store pixel locations.
		self.typeList=[]
		self.blobList=[]
		self.outerList=[]
		# Current pixel selected, as (x, y) tuple.
		self.pix=None
		# 0 = filling binType, 1 = filling blob, 2 = filling background
		self.stage=0
		# current blob being filled
		self.blobNum=0
		# Unscaled sigma values for pixel and color selection.
		self.sigma=sigma
		self.shaderSigma=shaderSigma
		# Path of image file.
		self.dirPath=dirPath
		# Name of image file.
		self.name=name
		# Stores pixel locations.
		self.startPT=[]
		# Minimum allowable pixel distance between 2 blobs.
		self.betweenBlobs=betweenBlobs
		# True/False, True means blobs are not allowed to touch image borders.
		self.touchingEdge=touchingEdge
		# True/False, ets all background pixels to pure blue for class A images.
		self.flatBG=flatBG
		# True/False, True applies a smoothing filter to images.
		self.filterOn=filterOn
		# True/False, True changes color scheme of image for certain class D images.
		self.addColors=addColors

	# Returns True if pixel at (x, y) is at least rad pixels from
	# any other blobs, else returns False.
	def clearSurrounding(self, x, y, rad):
		pixVal=[0, self.blobNum]
		for i in range(1+2*rad):
			a=i-rad
			for j in range(1+2*rad):
				b=j-rad
				if((0<=a+x<IMGSIZE) and (0<=b+y<IMGSIZE)):
					if(self.imgType[a+x][b+y] not in pixVal):
						return False
		return True

	# Finds a legal new pixel to add to shape, or add color to depending on stage of algorithm
	# and sets self.pix to new pixel location. Returns false if there are no avalible pixels,
	# else returns true.
	def getPix(self,size):
		# If choosing first pixel in shape.
		if(self.pix==None):
			if(self.touchingEdge==False):
				found=False
				while(found==False):
					a=random.randint(0, (IMGSIZE-1))
					b=random.randint(0, (IMGSIZE-1))
					if(self.clearSurrounding(a, b, self.betweenBlobs)==True):
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
		# If finding pixels to add to shape.
		if(self.stage==0):
			localSigma=len(self.typeList)*(self.sigma/50)
			x=int(random.gauss(len(self.typeList), localSigma))
			if(x>len(self.typeList)):
				x=len(self.typeList)-(x-len(self.typeList))
			x=x-1
			if(x<0):
				x=0
			if(len(self.typeList)==0):
				return False
			self.pix=self.typeList[x]
			self.typeList.remove(self.pix)
			return True
		# If choosing pixels in shape/background to color.
		if(self.stage==1):
			if(len(self.blobList)==0):
				return False
			localSigma=len(self.blobList)*(self.sigma/50)
			x=int(random.gauss(len(self.blobList)/2, localSigma))
			if(x>len(self.blobList)):
				x=len(self.blobList)-(x-len(self.blobList))
			x=x-1
			self.pix=self.blobList.pop()
			return True

	# Returns True if pixel location is not within 3 pixels of image border,
	# else returns False.
	def isEdge(self, pix):
		coords=[0,1,2,IMGSIZE-3,IMGSIZE-2,IMGSIZE-1]
		if(((pix[0] in coords) or (pix[1] in coords)) and self.touchingEdge==True):
			return False
		else:
			return True

	# Adds legal neighbors to list of neighboring pixels
	def addNeighbors(self):
		neighborList=[]
		pix=self.pix
		if(self.stage==0):
			currentList=self.typeList
			pixType=0
		if(self.stage==1):
			currentList=self.blobList
			pixType=self.blobNum
		# Add neighbors above, below, left, and right.
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
		# Add neighbors on 4 diagonals with probability 0.5.
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
			self.blobList.extend(neighborList)
	
	# Returns a list of all pixels in the background accessable by a BFS starting from image's
	# edge pixels. Note that if a "hole" contains a pixel along the border of the image it is
	# not considered a hole.					
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
			i=vertices.pop(0)
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

	# Returns a list of pixels in holes using the list of background pixels
	# obtained from the holeBFS() method.
	def fillHoleBFS(self, visited):
		toFill=[]
		for i in range(IMGSIZE):
			for j in range(IMGSIZE):
				if(visited[i][j]!=1 and self.imgType[i,j]==0):
					toFill.append((i,j))
		return toFill

	# Returns a list of pixels in a given blob or background, sorted by distance from
	# "center of mass" of blob/background. This "center of mass" is the pixel with ~equal
	# numbers of pixels below, above, left, and right.
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
			# Width balancing
			lWeight=0
			rWeight=0
			l=i-1
			r=i+1
			while(l>=0):
				lWeight=lWeight+wWeight[l]
				l=l-1
			while(r<IMGSIZE):
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

	# Returns a tuple of min and max allowable color intenseties for a given
	# pixel, as well as the average color intensity of neighboring pixels in the
	# same blob/background.
	def getLegalShades(self):
		if(self.imgType[self.pix[0], self.pix[1]]==0):
			if(self.flatBG==True):
				shades=[1,1]
			else:
				shades=[1, 255-self.blobThresh]
		else:
			shades=[self.blobThresh+1, 255]
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
					if(self.imgPlot[a, b]==0):
						continue
					# Make sure blob thresh can be met by any border cells.
					if (self.imgType[a,b]==0 and shades[1]>255-self.blobThresh):
						shades[1]=255-self.blobThresh
					if (self.imgType[a,b]>0 and shades[0]<1+self.blobThresh):
						shades[0]=self.blobThresh+1
					if(self.imgType[a,b]!=self.imgType[self.pix[0], self.pix[1]] and self.imgPlot[a, b]!=0):
						if(self.imgType[a,b]==0):#In a blob next to non-blob
							if(shades[0]>(self.imgPlot[a,b]+self.blobThresh)):
								shades[0]=self.imgPlot[a,b]+self.blobThresh
						if(self.imgType[a,b]!=0):#In non-blob next to blob
							if(shades[1]>(self.imgPlot[a,b]-self.blobThresh)):
								shades[1]=self.imgPlot[a,b]-self.blobThresh
					if(self.imgType[a,b]==self.imgType[self.pix[0], self.pix[1]] and self.imgPlot[a, b]!=0):
						avgShade[0]=avgShade[0]+1
						avgShade[1]=avgShade[1]+self.imgPlot[a, b]
						if(shades[0]<(self.imgPlot[a,b]-self.innerThresh)):
							shades[0]=self.imgPlot[a,b]-self.innerThresh
						if(shades[1]>(self.imgPlot[a,b]+self.innerThresh)):
							shades[1]=self.imgPlot[a,b]+self.innerThresh
		if(shades[0]>shades[1]):
					x=(shades[0]+shades[1])/2
					shades[0]=x
					shades[1]=x
		if(avgShade[0]!=0):
			# If neighboring pix are shaded already, let their colors influence
			avgShade=avgShade[1]/avgShade[0]
		else:
			# Otherwise pick random allowable color instead of local average
			avgShade=random.randint(shades[0], shades[1])
		# print avgShade
		return (shades[0], shades[1]), avgShade
	
	# Picks a color value for each pixel and records it.	
	def fillShades(self):
		for i in range(self.numBlob+1):
			pixList=self.getList(i)
			for j in pixList:
				self.pix=j
				shades, avgShade=self.getLegalShades()
				avgShade=np.clip([avgShade], shades[0], shades[1])
				avgShade=avgShade[0]
				sig=int((float(self.shaderSigma)/100)*(shades[1]-shades[0]))
				x=int(random.gauss(avgShade, sig))
				if(x>shades[1]):
					x=shades[1]-(x-shades[1])
				if(x<shades[0]):
					x=shades[0]
				self.imgPlot[self.pix[0], self.pix[1]]=x


	# Main method.
	def makeImg(self):
		img=Image.new('RGB', (IMGSIZE,IMGSIZE), 'white')
		print 'Making image: '+self.name

		# Choose which pixels belong to which blobs.
		for i in range(self.numBlob):
			self.blobNum=i+1
			blobSize = random.randint(self.minSize, self.maxSize)
			for j in range(blobSize):
				if(self.getPix(blobSize)==False):
					break
				# Find first pixel for blob i.
				if(j==0):
					if(self.clearSurrounding(self.pix[0], self.pix[1], IMGSIZE*(1/3))==False):
						goodPix=False
						while(goodPix==False):
							if(self.getPix(blobSize)==False):
								break
							if(self.clearSurrounding(self.pix[0], self.pix[1], IMGSIZE*(1/3))==True):
								goodPix=True
				else:
					if(self.clearSurrounding(self.pix[0], self.pix[1], self.betweenBlobs)==False):
						goodPix=False
						while(goodPix==False):
							if(self.getPix(blobSize)==False):
								break
							if(self.clearSurrounding(self.pix[0], self.pix[1], self.betweenBlobs)==True):
								goodPix=True
				self.addNeighbors()
				self.imgType[self.pix[0], self.pix[1]] = self.blobNum

				# Search for holes
				if((j==(blobSize/2)) or (j==(3*blobSize/4)) or j==blobSize-1):
					visited=self.holeBFS()
					toFill=self.fillHoleBFS(visited)
					j=j-len(toFill)
					for k in toFill:
						self.imgType[k[0],k[1]]=self.blobNum

			self.pix=None
			self.typeList=[]
		# Begin choosing colors for each pixel.
		self.stage=1
		self.fillShades()
		toSave=img.load()

		# Change color scheme for certain class D images.
		if(self.addColors==True):
			# 0 - 1 and 2
			# 1 - randomly swap colors representing blobs/background
			# 2 - add third color (variable)
			colorMod=random.randint(0,2)
			if(colorMod==0):
				vals=[0,1,2]
				a=random.choice(vals)
				vals.remove(a)
				b=random.choice(vals)
				vals.remove(b)
				c=vals[0]
				for i in range(IMGSIZE):
					for j in range(IMGSIZE):
						toMix=[self.imgPlot[i,j],0,255-self.imgPlot[i,j]]
						toSave[i,j]=(toMix[a],toMix[b],toMix[c])
			elif(colorMod==1):
				if(bool(random.getrandbits(1))==True):
					green=random.randint(0,255)
					for i in range(IMGSIZE):
						for j in range(IMGSIZE):
							toSave[i,j]=(self.imgPlot[i,j],green,255-self.imgPlot[i,j])
				else:
					for i in range(IMGSIZE):
						for j in range(IMGSIZE):
							toSave[i,j]=(self.imgPlot[i,j],random.randint(0,255),255-self.imgPlot[i,j])
			elif(colorMod==2):
				if(bool(random.getrandbits(1))):
					vals=[0,1,2]
					a=random.choice(vals)
					vals.remove(a)
					b=random.choice(vals)
					vals.remove(b)
					c=vals[0]
					for i in range(IMGSIZE):
						for j in range(IMGSIZE):
							toMix=[self.imgPlot[i,j],random.randint(0,255),255-self.imgPlot[i,j]]
							toSave[i,j]=(toMix[a],toMix[b],toMix[c])
				else:
					vals=[0,1,2]
					a=random.choice(vals)
					vals.remove(a)
					b=random.choice(vals)
					vals.remove(b)
					c=vals[0]
					green=random.randint(0,255)
					for i in range(IMGSIZE):
						for j in range(IMGSIZE):
							toMix=[self.imgPlot[i,j],green,255-self.imgPlot[i,j]]
							toSave[i,j]=(toMix[a],toMix[b],toMix[c])

		else:
			for i in range(IMGSIZE):
				for j in range(IMGSIZE):
					toSave[i,j]=(self.imgPlot[i,j],0,255-self.imgPlot[i,j])

		# Apply smoothing filter if class A img.
		if(self.filterOn==True):
			img=img.filter(ImageFilter.BLUR)
		img.save(self.dirPath + '/' + self.name + '.png')

