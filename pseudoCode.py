L = current length of neighbor list
localSigma = L * (sigma/50)
x = Gaussian of mu L and standard deviation sigma
If(x > L):
	x = L - (x - L)
x = x - 1
If(x < 0):
	x = 0
nextPixel = neighborList [x]






typeArray = 2d array of pixels by type (blob/background)
colorArray = 2d array of pixel shade values

For(Number of blobs):

	-Randomly pick blob size using supplied upper/lower bounds.

	For(Number of pixels in blob):

		If(picking first pixel):

			-Pick random pixel in background

		else:

			-Pick pixel from list of neighboring pixels

		-Check to ensure that pixel is not touching other blobs
		-Add pixel location to type array as type blob

		If(blob is half, 3/4, or almost completely filled):

			-Fill any holes in the blob, and subtract the number of
			filled pixels from the remaining pixels left to fill in
			parent iterator.

	-Add all of the pixels in current blob to a list of pixel coordinates,
		sorted by distance from the center of the blob.
	For(List of pixels in blob):

		-Get allowable color range by looking at neighboring pixels
		-Get average color shade of neighboring pixels if possible
		-Pick color shade in range of allowable shades

If(Change color scheme (Occurs on certain class D images)):
	Randomly do one of the 3 following modifications:

		-Randomly pick blob and background colors from R, G, and B.
		-Add either a constant or random G value to all pixels
		-Do both of the above
else

	Fill .png image with blue for low color shade values and red for high
		color shade values.




