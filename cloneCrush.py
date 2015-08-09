# Created by: Melanie Hsu (bluemelodia)

# A class that looks through a directory to find and rank images that are similar in texture and/or color
# to a user-provided query image.  

from sklearn.cluster import KMeans
import matplotlib.pyplot as pyplot 
import math
import random
import numpy as np
import scipy
import argparse
import cv2
import os
import operator
import PIL
import re
import sys
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import imghdr as I

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

# round each pixel value so it fits into one of the bins
def rnd(x):
	base = 32
	return int(base*math.floor(float(x)/base))/base

#calculate the L1_Norm between a pair of images
#0.0 - perfect similarity
def L1norm(A, B, Awidth, Aheight, Bwidth, Bheight):
	sum = Awidth*Aheight + Bwidth*Bheight
	distance = 0

	for i in range(0, 8):
		for j in range(0, 8):
			for k in range(0, 8):
				if i == 0 and j == 0 and k == 0:
					if math.fabs(A[0,0,0] - B[0,0,0]) < 100:
						sum -= A[0,0,0]
						sum -= B[0,0,0]
						continue
				distance += math.fabs(A[i,j,k] - B[i,j,k])
	norm = distance/sum
	return norm

def cloneCrusher(imageDir, directory, queryImage, destDir, flag):
	# necessary check to see if the image can be used to query
	queryPath = os.path.abspath(queryImage)

	# step through all files in directory
	path, dirs, files = os.walk(imageDir).next()

	# initialize the progress variables
	total = len(files)
	count = 0
	progress = 0

	# initialize the progress bar
	progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	# store the distance
	differences = {}
	differences[0] = queryPath

	# make a histogram
	hist = {}
	queryImg = Image.open(queryImage)
	pix = queryImg.load()

	for i in range(0, 8):
		for j in range(0, 8):
			for k in range(0, 8):
				hist[(i, j, k)] = 0

	width, height = queryImg.size
	for i in range(0, width):
		for j in range(0, height):
			pixel = pix[i, j]
			blue = rnd(pixel[0])
			green = rnd(pixel[1])
			red = rnd(pixel[2])
			hist[(blue, green, red)] += 1

	validPics = 1
	for file in files:
		path = imageDir + "/" + file
		# update progress and display it to the user
		count += 1	

		if I.what(path) != None:
			validPics += 1

			otherHist = {}
			otherImg = Image.open(path)
			pix = otherImg.load()

			for i in range(0, 8):
				for j in range(0, 8):
					for k in range(0, 8):
						otherHist[(i, j, k)] = 0

			otherWidth, otherHeight = otherImg.size
			for i in range(0, otherWidth):
				for j in range(0, otherHeight):
					pixel = pix[i, j]
					blue = rnd(pixel[0])
					green = rnd(pixel[1])
					red = rnd(pixel[2])
					otherHist[(blue, green, red)] += 1
			norm = round(L1norm(hist, otherHist, width, height, otherWidth, otherHeight), 5)
			differences[norm] = path
			progress.update((float(count)/total)*100)
		else:
			progress.update((float(count)/total)*100)
			continue
	progress.finish()
	print "\nFinished image similarity calculations.\n"