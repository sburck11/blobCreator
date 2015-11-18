import random
import numpy as np

# mu = 125
# sigma = 25

# for i in range(20):
# 	x=random.gauss(mu, sigma)
# 	if (x>mu):
# 		x=125-(x-125)
# 	if(x<0):
# 		x=0
# 	print x
# array = np.zeros((100, 100), dtype = np.int)
# print array
# array[0][0] = 1
# print array

# a = random.randint(0, 255)
# b = random.randint(0, 255)
# print a
# print b

# x=b-(x-b)

# rand = 10
# len = 7

# len - (rand-len

# IMGSIZE=10
# imgType=[[0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
#  [0, 0, 0, 0, 2, 2, 2, 2, 0, 0],
#  [1, 0, 0, 0, 0, 0, 2, 2, 0, 0],
#  [1, 1, 0, 0, 0, 2, 2, 0, 0, 0],
#  [1, 1, 1, 1, 0, 0, 2, 0, 0, 0],
#  [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
#  [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#  [1, 1, 1, 0, 0, 0, 0, 0, 0, 0],
#  [1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
#  [1, 1, 1, 0, 0, 0, 0, 0, 0, 0]]
# def getList(blobNum):
# 	center=[0.0,0.0]
# 	wWeight=[0]*IMGSIZE
# 	hWeight=[0]*IMGSIZE
# 	blobList=[]
# 	for i in range(IMGSIZE):
# 		for j in range(IMGSIZE):
# 			if(imgType[i][j]==1):
# 				blobList.append((i,j))
# 				wWeight[i]=wWeight[i]+1
# 				hWeight[i]=hWeight[i]+1
# 	wPoint=0
# 	hWeight=0
# 	wBal=np.zeros((IMGSIZE), dtype=np.int)
# 	hBal=np.zeros((IMGSIZE), dtype=np.int)
# 	for i in range(IMGSIZE):
# 		# Width balancing
# 		lWeight=0
# 		rWeight=0
# 		l=i-1
# 		r=i+1
# 		while(l<IMGSIZE):
# 			print wWeight
# 			lWeight=lWeight+wWeight[l]
# 			l=l+1
# 		while(r>0):
# 			rWeight=rWeight+wWeight[r]
# 			r=r-1
# 		wBal[i]=abs(rWeight+lWeight)
# 		# Height balancing
# 		tWeight=0
# 		bWeight=0
# 		t=i+1
# 		b=i-1
# 		while(t<IMGSIZE):
# 			print hWeight
# 			tWeight=tWeight+hWeight[t]
# 			t=t+1
# 		while(b>0):
# 			bWeight=bWeight+hWeight[b]
# 			b=b-1
# 		hBal[i]=abs(tWeight+bWeight)
# 	wIndex=wBal.argmin()
# 	hIndex=hBal.argmin()
# 	blobList.sort(key=lambda x,y: abs(0-abs(x-wIndex)-abs(y-hIndex)))
# 	return blobList

# print getList(1)

a=random.randint(0,1)
if(a==0):
	print 'iPhone!'
else:
	print 'Droid!'