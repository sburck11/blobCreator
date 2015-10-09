from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
from blobClass.blob import Blob

numBlob=3
minSize=8000
maxSize=1800
blobThresh=100
innerThresh=50
sigma=55
shaderSigma=30
betweenBlobs=5
path='/Users/Sam/Desktop/regenProj/blobCreator/GS_Images'

# testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
# 		sigma, path, betweenBlobs, 'test')
# testImage.makeImg()

for i in range(25):
	print i
	# sigma = (1.2*i)+1
	numBlob=random.randint(1, 4)
	sigma=random.randint(45, 80)
	shaderSigma=random.randint(10, 100)
	minSize=random.randint(100, 500)
	maxSize=random.randint(800, 2000)
	blobThresh=random.randint(50, 150)
	innerThresh=random.randint(20, 120)
	name='img_' + str(i) + '_sigma_' + str(sigma)
	testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
		sigma, shaderSigma, path, betweenBlobs, name)
	testImage.makeImg()