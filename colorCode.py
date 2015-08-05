# Created by: Melanie Hsu (bluemelodia)

from sklearn.cluster import KMeans
import matplotlib.pyplot as pyplot 
import argparse
import cv2
import os
import sys
from PIL import Image
import imghdr as I

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

def dominantColors(listDir, directory, destDir):
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
		path = directory + "/" + imgpath

		# update progress and display it to the user
		count += 1

		if I.what(path) != None:
			imagePath = directory + "/" + imgpath

			# load the image nand convert it from BGR to RGB, enabling display with matplotlib
			image = cv2.imread(imagePath)
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

			# show image
			pyplot.figure()
			pyplot.axis("off")
			pyplot.imshow(image)
			pyplot.show()

			bar.update((float(count)/total)*100)
		else:
			bar.update((float(count)/total)*100)
			continue
	bar.finish()