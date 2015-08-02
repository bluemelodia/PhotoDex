from __future__ import division
from PIL import Image
import imghdr as I
import cv2
import sys
import os
import math

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

cascades = []

#detect faces in the provided image
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

	#loop over the bounding boxes, draw a rectangle around the faces
	#where (x, y) is the starting location of the face
	for (x, y, w, h) in faces:
		cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    		roi_gray = gray[y:y+h, x:x+w]
    		roi_color = img[y:y+h, x:x+w]
	cv2.imshow("Faces", img)
	cv2.waitKey(0)
	cv2.destroyAllWindows()
	return len(faces)

def cascade():
	# create the haar cascade and initialize it with our face cascade
	# each cascade is an XML file that contains the data to detect faces
	if sys.argv[2] == 'P':
		faceCascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
		faceCascade2 = cv2.CascadeClassifier('haarcascade_frontalface.alt.xml')
		faceCascade3 = cv2.CascadeClassifier('haarcascade_frontalface.alt2.xml')
		cascades.append(faceCascade)
		cascades.append(faceCascade2)
		cascades.append(faceCascade3)

	# initialize array of accepted image types

def detectLife(listDir, directory, types):
	#step through all files in directory
	path, dirs, files = os.walk(sys.argv[1]).next()

	#initialize the progress variables
	total = len(files)
	count = 0
	progress = 0
	faceCount = 0 # number of photos that contain faces

	#initialize the progress bar
	bar = ProgressBar(widgets=[Percentage(), Bar()], maxval=total).start()


	for imgpath in listDir:
		# display progress to the user
		bar.update(count)

		path = sys.argv[1] + "/" + imgpath
		if I.what(path) in types: # is this an accepted image type?
			for cascade in cascades:
				faces = detection(cascade, directory + "/" + imgpath)
				# we know there is a face, no need to try subsequent cascades
				if faces >= 1:			
					print "Found a face"
			else:
				continue
	bar.finish()

