from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
from blobClass.blob import Blob

numBlob=2
minSize=800
maxSize=1200
blobThresh=130
innerThresh=190
sigma=120
shaderSigma=5
betweenBlobs=5
path='/Users/Sam/Desktop/regenProj/blobCreator/Make_1'
name='edgeToEdge'
filterOn=False
flatBG=False
touchingEdge=False
addColors=False


testImage=Blob(numBlob, minSize, maxSize, blobThresh, innerThresh,
			sigma, shaderSigma, path, betweenBlobs, touchingEdge, flatBG, filterOn, addColors, name)
testImage.makeImg()


