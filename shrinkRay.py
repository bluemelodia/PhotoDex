# A handy ray that will shrink the size of your images

import cv2

def shrinkByWidth(image, width):
	img = cv2.imread(image)

	# preserve aspect ratio so the image does not look skewed or distorted 
	ratio = img.shape[0]/float(img.shape[1])
	dimension = (width, (width*img.shape[0])/img.shape[1])

	# resize the image
	resizedImg = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA)
	
	# overwrite the old image
	cv2.imwrite(image, resizedImg)

def shrinkByHeight(image, height):
	img = cv2.imread(image)

	# preserve aspect ratio so the image does not look skewed or distorted 
	ratio = img.shape[0]/float(img.shape[1])
	print "ratio: " + str(ratio)
	print "height: " + str(height)
	print "original dimensions: " + str(img.shape[0]) + " " + str(img.shape[1])

	dimension = ((height*img.shape[1])/img.shape[0], height)
	print (height*img.shape[0])/img.shape[1]
	print dimension

	# resize the image
	resizedImg = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA)
	print "new dimensions: " + str(resizedImg.shape[0]) + " " + str(resizedImg.shape[1])


	# overwrite the old image
	cv2.imwrite(image, resizedImg)