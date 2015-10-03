from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
from blobClass.blob import Blob

numBlob=3
minSize=8000
maxSize=1800
blobThresh=50
innerThresh=50
sigma=55
path='/Users/Sam/Desktop/regenProj/blobCreator/Images'

# testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
# 		sigma, path, 'test')
# testImage.makeImg()

for i in range(20):
	print i
	# sigma = (1.2*i)+1
	sigma=20
	minSize=random.randint(500, 1000)
	maxSize=random.randint(1300, 2000)
	name='img_' + str(i) + '_sigma_' + str(sigma)
	testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
		sigma, path, name)
	testImage.makeImg()