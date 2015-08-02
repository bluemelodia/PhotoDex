# Created by: Melanie Hsu (bluemelodia)

# A handy ray that will shrink the size of your images
# If calling through 'R' protocol, supply a size argument to main as the last argument
# Example:  python main.py ../Profile_Pictures R ../Art 500

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

	dimension = ((height*img.shape[1])/img.shape[0], height)

	# resize the image
	resizedImg = cv2.resize(img, dimension, interpolation = cv2.INTER_AREA)

	# overwrite the old image
	cv2.imwrite(image, resizedImg)

def shrinkImages(listDir, directory):
	print "Shrinking your stuff..."