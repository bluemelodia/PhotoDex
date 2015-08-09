# Created by: Melanie Hsu (bluemelodia)

# A handy ray that will shrink the size of all images in the provided directory
# Example call:
# Relative Path to Source Directory: ../Profile_Pictures_Original
# Relative Path to Destination Directory: ../Profile_Pictures_Original
# I choose: S
# Enter your impossible-to-attain ideal size: 500
# Do you want them short or skinny? ('H' - height/'W' - width): W

import cv2
import os
from PIL import Image
import imghdr as I

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

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

def shrinkImages(listDir, directory, size, flag):
	# step through all files in directory
	path, dirs, files = os.walk(listDir).next()

	# initialize the progress variables
	total = len(files)
	count = 0
	progress = 0

	# initialize the progress bar
	bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	for file in files:
		path = listDir + "/" + file

		# update progress and display it to the user
		count += 1

		if I.what(path) != None:
			if (flag == 'H'):
				imagePath = shrinkByWidth(path, int(size))
			else:
				imagePath = shrinkByHeight(path, int(size))
			bar.update((float(count)/total)*100)
		else:
			bar.update((float(count)/total)*100)
			continue
	bar.finish()
	print "\nHoney, I shrunk the directory!\n"
