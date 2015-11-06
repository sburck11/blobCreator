from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
import threading
from blobClass.blob import Blob
from pathos.multiprocessing import ProcessingPool

numBlob=2
minSize=800
maxSize=1800
blobThresh=100
innerThresh=50
sigma=55
shaderSigma=30
betweenBlobs=5
path='/Users/Sam/Desktop/regenProj/blobCreator/set_1'
# 'mp' for multiprocessing, 'mt' for multithreading
MODE='mp'


# Multithreading
if(MODE=='mp'):
	# 1 sec/img for nodes=4

	pool=ProcessingPool(nodes=4)	
	imgArr=[]
	for i in range(50):
		# print i
		# sigma = (1.2*i)+1
		type=random.randint(1,4)
		# type=2
		# numBlob=random.randint(1, 2)
		# FALSE
		if(type==4):
			# GRADE D
			filterOn=False
			flatBG=False
			numBlob=random.randint(0, 3)
			if(numBlob==1):
				numBlob=random.randint(2,3)
			touchingEdge=False
			sigma=random.randint(5, 40)
			shaderSigma=random.randint(1, 150)
			minSize=random.randint(800, 1000)
			maxSize=random.randint(1000, 3000)
			blobThresh=random.randint(30, 120)
			innerThresh=random.randint(40, 180)
			name='D_'+str(i)
		elif(type==3):
			# Grade C
			filterOn=False
			flatBG=False
			touchingEdge=False
			flaw=random.randint(0,2)
			if(flaw==0):
				# 1 Blob
				numBlob=1
				touchingEdge=True
				sigma=50
				shaderSigma=random.randint(40, 100)
				blobThresh=random.randint(100, 120)
				innerThresh=random.randint(120, 180)
				minSize=random.randint(400, 600)
				maxSize=random.randint(800, 1200)
				# name='C0_'+str(i)
			elif(flaw==1):
				# Not Jagged
				numBlob=random.randint(2,3)
				sigma=random.randint(130, 180)
				shaderSigma=random.randint(25, 50)
				blobThresh=random.randint(100, 120)
				innerThresh=random.randint(70, 90)
				minSize=random.randint(500, 800)
				maxSize=random.randint(1000, 1500)
				# name='C1_'+str(i)
			else:
				# Not Speckled
				flatBG=True
				numBlob=random.randint(2,3)
				minSize=random.randint(500, 800)
				maxSize=random.randint(1000, 1250)
				sigma=50
				shaderSigma=random.randint(100, 150)
				blobThresh=random.randint(120, 150)
				innerThresh=random.randint(5, 15)
				# name='C2_'+str(i)
			name='C_'+str(i)
		# MARGINAL
		elif(type==2):
			# Grade B
			filterOn=False
			numBlob=1
			touchingEdge=False
			flaw=random.randint(0,2)
			if(flaw==0):
				# 1 Blob, Not Jagged
				numBlob=1
				touchingEdge=True
				flatBG=False
				filterOn=True
				sigma=random.randint(130, 250)
				shaderSigma=random.randint(25, 50)
				blobThresh=random.randint(100, 120)
				innerThresh=random.randint(40, 60)
				minSize=random.randint(400, 600)
				maxSize=random.randint(800, 1200)
				# name='B0_'+str(i)
			elif(flaw==1):
				# 1 Blob, Not Speckled
				numBlob=1
				flatBG=True
				touchingEdge=True
				filterOn=False
				sigma=50
				shaderSigma=random.randint(5, 20)
				blobThresh=random.randint(150, 180)
				innerThresh=random.randint(5, 10)
				minSize=random.randint(750, 1000)
				maxSize=random.randint(1500, 2000)
				# name='B1_'+str(i)
			else:
				# Mult blobs, Not Jagged, Not Speckled
				numBlob=random.randint(2,3)
				filterOn=True
				flatBG=True
				touchingEdge=False
				sigma=random.randint(160, 225)
				shaderSigma=random.randint(15, 20)
				minSize=random.randint(500, 750)
				maxSize=1000
				blobThresh=random.randint(150, 180)
				innerThresh=random.randint(10, 25)
				# name='B2_'+str(i)
			name='B_'+str(i)
		# TRUE
		else:
			# GRADE A
			filterOn=True
			flatBG=True
			numBlob=1
			touchingEdge=True
			sigma=120
			shaderSigma=random.randint(15, 20)
			minSize=random.randint(500, 750)
			maxSize=random.randint(1000, 2000)
			blobThresh=random.randint(180, 250)
			innerThresh=random.randint(10, 20)
			name='A_'+str(i)

		#name='Img-'+str(i)+'_numBlob-'+str(numBlob)+'_sigma-'+str(sigma)+'_shaderSigma-'+str(shaderSigma)+'_minSize-'+str(minSize)+'_maxSize-'+str(maxSize)+'_blobThresh-'+str(blobThresh)+'_innerThresh-'+str(innerThresh)
		# if(numBlob==1):
		# 	name='TRUE_'+str(i)
		# else:
		# 	name='FALSE_'+str(i)
		testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
			sigma, shaderSigma, path, betweenBlobs, touchingEdge, flatBG, filterOn, name)
		imgArr.append(testImage)

	pool.map(Blob.makeImg, imgArr)

# else:
# 	threads=[]
# 	for i in range(25):
# 		# print i
# 		# sigma = (1.2*i)+1
# 		numBlob=random.randint(2, 2)
# 		sigma=random.randint(105, 225)
# 		shaderSigma=random.randint(15, 35)
# 		minSize=random.randint(250, 1000)
# 		maxSize=random.randint(1200, 1800)
# 		blobThresh=random.randint(100, 150)
# 		innerThresh=random.randint(30, 55)
# 		name='Img-'+str(i)+'_numBlob-'+str(numBlob)+'_sigma-'+str(sigma)+'_shaderSigma-'+str(shaderSigma)+'_minSize-'+str(minSize)+'_maxSize-'+str(maxSize)+'_blobThresh-'+str(blobThresh)+'_innerThresh-'+str(innerThresh)
# 		testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
# 			sigma, shaderSigma, path, betweenBlobs, name)
		
# 		mythread=threading.Thread(target=testImage.makeImg)
# 		mythread.setDaemon(True)
# 		threads.append(mythread)
# 		mythread.start()
# 		print threading.activeCount()

# 	for i in threads:
# 		i.join()
