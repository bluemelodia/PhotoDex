# Created by: Melanie Hsu (bluemelodia)

# To run this protocol, supply an additional fifth argument, Y - show or N - no show
# This will determine whether the photos are displayed in a window

# Example: python main.py
# Relative Path to Source Directory: ../iPhone_Photo_Short
# Relative Path to Destination Directory: ../Sentient_Beings
# I choose: F
#    N

from __future__ import division
from PIL import Image
import imghdr as I
import cv2
import sys
import os
import math

import shrinkRay

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

cascades = []
showPhotos = None

# detect faces in the provided image
def detection(cascade, image):
	# read the image
	img = cv2.imread(image)
	if img is None or len(img.shape) <= 0:
		return 0

	gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	# detect faces in the image
	# detectMultiScale: general function that detects objects, depends on provided cascade
	# scaleFactor: compensates for foreground vs. background faces
	# minNeighbors: # objects that must be detected near the current one before it detects the face
	faces = cascade.detectMultiScale(
		gray, 
		scaleFactor = 1.3, 
		minSize = (50, 50),
		minNeighbors = 5,
		flags = cv2.cv.CV_HAAR_SCALE_IMAGE
	)

	# loop over the bounding boxes, draw a rectangle around the faces
	# where (x, y) is the starting location of the face
	for (x, y, w, h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = img[y:y+h, x:x+w]

    	# only show this if the user specified 'Y' as the flag
    	if (showPhotos == 'Y'):
			cv2.imshow("Faces", img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
    	return len(faces)

def cascade():
	# these files must be in the same directory as faceDetection.py for face detection to succeed
	cascades.append(cv2.CascadeClassifier('haarcascade_frontalface_default.xml'))
	cascades.append(cv2.CascadeClassifier('haarcascade_frontalface_alt.xml'))
	cascades.append(cv2.CascadeClassifier('haarcascade_frontalface_alt2.xml'))
	cascades.append(cv2.CascadeClassifier('haarcascade_frontalface_alt_tree.xml'))
	cascades.append(cv2.CascadeClassifier('haarcascade_profileface.xml'))

def detectLife(listDir, directory, flag, destDir):
	# set the display flag
	global showPhotos
	showPhotos = flag

	# step through all files in directory
	path, dirs, files = os.walk(listDir).next()

	# initialize the progress variables
	total = len(files)
	count = 0
	progress = 0
	faceCount = 0 # number of photos that contain faces

	# initialize the progress bar
	bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	for file in files:
		path = listDir + "/" + file

		# update progress and display it to the user
		count += 1

		if I.what(path) != None:
			# resize the image if its width exceeds 500 pixels
			image = Image.open(path)
			width, height = image.size
			if width > 500:
				imagePath = shrinkRay.shrinkByWidth(path, 500)

			for cascade in cascades:
				faces = detection(cascade, path)
				# if we know that there is a face, there's no need to try subsequent cascades
				if faces >= 1:			
					faceCount += 1
					os.rename(path, destDir + "/" + os.path.basename(path))
					break
			bar.update((float(count)/total)*100)
		else:
			bar.update((float(count)/total)*100)
			continue
	bar.finish()
	print "\nWe have discovered " + str(faceCount) + " humans.\n"