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
		type=random.randint(1,3)
		# type=2
		# numBlob=random.randint(1, 2)
		# FALSE
		if(type==3):
			isTrue=False
			numBlob=random.randint(2, 3)
			touchingEdge=False
			sigma=random.randint(30, 120)
			shaderSigma=random.randint(5, 80)
			minSize=random.randint(100, 1000)
			maxSize=random.randint(1000, 1800)
			blobThresh=random.randint(50, 120)
			innerThresh=random.randint(40, 180)
			name='FALSE_'+str(i)
		# MARGINAL
		elif(type==2):
			isTrue=False
			numBlob=1
			touchingEdge=False
			flaw=random.randint(0,2)
			if(flaw==0):
				touchingEdge=True
				sigma=random.randint(52, 55)
				shaderSigma=random.randint(15, 20)
				blobThresh=random.randint(100, 130)
				innerThresh=random.randint(25, 35)
			 	# name='MARGINAL_0_'+str(i)
				minSize=random.randint(400, 600)
				maxSize=random.randint(800, 1200)
			elif(flaw==1):
				sigma=random.randint(130, 180)
				shaderSigma=random.randint(25, 50)
				blobThresh=random.randint(100, 120)
				innerThresh=random.randint(70, 90)
				# name='MARGINAL_1_'+str(i)
				minSize=random.randint(750, 1000)
				maxSize=random.randint(1500, 2000)
			else:
				touchingEdge=True
				sigma=random.randint(52, 70)
				shaderSigma=random.randint(30, 60)
				blobThresh=random.randint(100, 120)
				innerThresh=random.randint(70, 90)
				# name='MARGINAL_2_'+str(i)
				minSize=random.randint(750, 1000)
				maxSize=random.randint(1500, 2000)
			name='MARGINAL_'+str(i)
		# TRUE
		else:
			isTrue=True
			numBlob=1
			touchingEdge=True
			sigma=random.randint(130, 225)
			shaderSigma=random.randint(15, 20)
			minSize=random.randint(500, 1000)
			maxSize=random.randint(1500, 3000)
			blobThresh=random.randint(150, 180)
			innerThresh=random.randint(10, 25)
			name='TRUE_'+str(i)

		#name='Img-'+str(i)+'_numBlob-'+str(numBlob)+'_sigma-'+str(sigma)+'_shaderSigma-'+str(shaderSigma)+'_minSize-'+str(minSize)+'_maxSize-'+str(maxSize)+'_blobThresh-'+str(blobThresh)+'_innerThresh-'+str(innerThresh)
		# if(numBlob==1):
		# 	name='TRUE_'+str(i)
		# else:
		# 	name='FALSE_'+str(i)
		testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
			sigma, shaderSigma, path, betweenBlobs, touchingEdge, isTrue, name)
		imgArr.append(testImage)
	pool.map(Blob.makeImg, imgArr)

else:
	threads=[]
	for i in range(25):
		# print i
		# sigma = (1.2*i)+1
		numBlob=random.randint(2, 2)
		sigma=random.randint(105, 225)
		shaderSigma=random.randint(15, 35)
		minSize=random.randint(250, 1000)
		maxSize=random.randint(1200, 1800)
		blobThresh=random.randint(100, 150)
		innerThresh=random.randint(30, 55)
		name='Img-'+str(i)+'_numBlob-'+str(numBlob)+'_sigma-'+str(sigma)+'_shaderSigma-'+str(shaderSigma)+'_minSize-'+str(minSize)+'_maxSize-'+str(maxSize)+'_blobThresh-'+str(blobThresh)+'_innerThresh-'+str(innerThresh)
		testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
			sigma, shaderSigma, path, betweenBlobs, name)
		
		mythread=threading.Thread(target=testImage.makeImg)
		mythread.setDaemon(True)
		threads.append(mythread)
		mythread.start()
		print threading.activeCount()

	for i in threads:
		i.join()

# Multiprocessing


