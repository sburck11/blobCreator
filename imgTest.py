from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import random
from blobClass.blob import Blob

# imgArr = np.array([
# [0,0,0,0,1,1,1,1],
# [0,0,0,0,1,1,1,1],
# [0,0,0,0,1,1,1,1],
# [0,0,0,0,1,1,1,1],
# [0,0,0,0,1,1,1,1],
# [0,0,0,0,1,1,1,1],
# [0,0,0,0,1,1,1,1],
# [0,0,0,0,1,1,1,1]
# ])

# imgArr=[]
# img = Image.new('1', (1000,1000), 'black')
# pixels=img.load()

# for x in range(img.size[0]):
# 	for y in range(img.size[1]):
# 		x=int(x)
# 		y=int(y)
# 		if(y<500):
# 			pixels[x,y]=(0)
# 		else:
# 			pixels[x,y]=(1)
# # 	imgArr.append(rowArr)
# # imgArr=np.asarray(imgArr)

# # im=Image.fromarray(imgArr, mode='1')
# img.save("testImg.png")

# plt.imshow(imgArr)
# plt.savefig('testImg.bmp')

numBlob=3
minSize=1000
maxSize=2300
outerThresh=50
blobThresh=50
innerThresh=50
sigma=55
path='/Users/Sam/Desktop/regenProj/blobCreator'

testImage=Blob(numBlob, minSize, maxSize, outerThresh, blobThresh, innerThresh,
		sigma, path, 'test')
testImage.makeImg()

# for i in range(100):
# 	print i
# 	sigma = (1.25*i)+1
# 	minSize=random.randint(500, 1000)
# 	maxSize=random.randint(1500, 5000)
# 	name='img_' + str(i) + '_sigma_' + str(sigma)
# 	testImage=Blob(numBlob, minSize, maxSize, outerThresh, blobThresh, innerThresh,
# 		sigma, path, name)
# 	testImage.makeImg()