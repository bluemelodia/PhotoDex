# Created by: Melanie Hsu (bluemelodia)

# In order to run the face detection algorithm, a fifth argument is necessary:
# a directory containing the haar cascade XML files
# Example: python main.py ../Profile_Pictures F ../Art cascades

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

#TODO: use a larger library, ensure the progress bar is working

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
		scaleFactor = 1.4, 
		minNeighbors = 5, 
	)

	#print faces

	# loop over the bounding boxes, draw a rectangle around the faces
	# where (x, y) is the starting location of the face
	for (x, y, w, h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = img[y:y+h, x:x+w]
	#cv2.imshow("Faces", img)
	#cv2.waitKey(0)
	#cv2.destroyAllWindows()
	return len(faces)

def cascade():
	try:
		cDir = os.listdir(sys.argv[4])
	except:
		print "ERROR: Your cascades directory was accidentally pulverised.\n"
		sys.exit()

	# create the haar cascade and initialize it with our face cascade
	# each cascade is an XML file that contains the data to detect faces
	for cascadeFile in cDir:
		cascades.append(cv2.CascadeClassifier(cascadeFile))

def detectLife(listDir, directory):
	# step through all files in directory
	path, dirs, files = os.walk(sys.argv[1]).next()

	# initialize the progress variables
	total = len(files)
	count = 0
	progress = 0
	faceCount = 0 # number of photos that contain faces

	# initialize the progress bar
	bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	for imgpath in listDir:
		path = sys.argv[1] + "/" + imgpath

		# update progress and display it to the user
		count += 1
		bar.update((float(count)/total)*100)

		if I.what(path) != None:
			# resize the image if its width exceeds 500 pixels
			imagePath = directory + "/" + imgpath
			image = Image.open(imagePath)
			width, height = image.size
			if width > 500:
				imagePath = shrinkRay.shrinkByWidth(imagePath, 500)

			for cascade in cascades:
				faces = detection(cascade, imagePath)
				# we know there is a face, no need to try subsequent cascades
				if faces >= 1:			
					print "Found a face"
					faceCount += 1
					continue
		else:
			continue
	bar.finish()
	print "\nWe have discovered " + str(faceCount) + " humans.\n"
