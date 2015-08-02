# A handy ray that will shrink the size of your images

import cv2

def shrink(image, width):
	img = cv2.imread(image)

	# preserve aspect ratio so the image does not look skewed or distorted 
	ratio = img.shape[0]/float(img.shape[1])
	dimension = (width, (width*img.shape[0])/img.shape[1])
	print img.shape
	print ratio
	print dimension

	# resize the image
	resizedImg = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA)
	
	# overwrite the old image
	cv2.imwrite(image, resizedImg)


