from PIL import Image

img=Image.new('RGB', (256,256), 'white')
toSave=img.load()

for i in range(256):
	for j in range(256):
		toSave[i,j]=(i,0,255-i)


img.save('colorTest.png')