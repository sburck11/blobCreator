from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
from blobClass.blob import Blob

numBlob=1
minSize=1200
maxSize=4000
blobThresh=120
innerThresh=60
sigma=120
shaderSigma=40
betweenBlobs=5
path='/Users/Sam/Desktop/regenProj/blobCreator/Make_1'
name='InnerThresh-20__Sigma-'

testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
		sigma, shaderSigma, path, betweenBlobs, name)
testImage.makeImg()


