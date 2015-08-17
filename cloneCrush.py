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
from collections import OrderedDict
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

# This shouldn't be relying on a query - you have to calculate whether each image is related to any other*
def cloneCrusher(imageDir, directory, destDir, flag):
	# step through all files in directory
	path, dirs, files = os.walk(imageDir).next()

	# take a count of how many valid pictures we have
	validPics = 0

	# make a record of how similar images are to each other
	similarities = {}

	# save the histogram of each image
	hist = {}

	# turn everything into the same format to enable image comparisons
	for file in files:
		path = imageDir + "/" + file
		if I.what(path) != 'png' and I.what(path) != 'ppm' and I.what(path) != 'jpg':
			continue
		splitpath = path.rsplit ('.', 1)
		newpath = str(splitpath[0]) + '.jpg'
		os.rename(str(path), str(newpath))

	for file in files:
		path = imageDir + "/" + file
		if I.what(path) != None:
			validPics += 1
			similarities[path] = {}
			hist[path] = {}

	print "Generating image color histograms.\n"

	# initialize the progress variables and bar
	count = 0
	progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	# iterate through each image, making and saving its histogram
	for key, value in similarities.items():
		count += 1
		thisHist = {}
		thisImage = Image.open(key)
		pix = thisImage.load()

		for i in range(0, 8):
				for j in range(0, 8):
					for k in range(0, 8):
						thisHist[(i, j, k)] = 0

		width, height = thisImage.size
		for i in range(0, width):
			for j in range(0, height):
				pixel = pix[i, j]
				blue = rnd(pixel[0])
				green = rnd(pixel[1])
				red = rnd(pixel[2])
				thisHist[(blue, green, red)] += 1
		hist[key] = thisHist # save the histogram
		progress.update((float(count)/validPics)*100)
	progress.finish()

	print "\nRunning DNA tests...\n"

	count = 0
	progressTwo = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	for key, value in hist.items():
		count += 1
		for otherKey, otherValue in hist.items():
			if key == otherKey and value == otherValue:
				continue
			thisImage = Image.open(key)
			thatImage = Image.open(otherKey)
			thisWidth, thisHeight = thisImage.size
			thatWidth, thatHeight = thatImage.size

			norm = round(L1norm(value, otherValue, thisWidth, thisHeight, thatWidth, thatHeight), 5)
			similarities[key][otherKey] = norm
			progressTwo.update((float(count)/validPics)*100)
		
		# sort the images from most to least similar to the base image
		similarities[key] = OrderedDict(sorted(similarities[key].items(), key=lambda x:x[1], reverse=False))
	progressTwo.finish()

	print "\nGenerating similarity rankings...\n"

	progressThree = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	font = ImageFont.load_default()
	bigImage = Image.new('RGB', (100*(validPics), 100*(validPics)))
	draw = ImageDraw.Draw(bigImage)

	keyCount = 0 # track iterations in the outer loop

	# create an image showing all image similarities to each other
	for key, value in similarities.items():
		basewidth = 100
		baseImage = Image.open(key)
		wpercent = (basewidth / float(baseImage.size[0]))
		hsize = int((float(baseImage.size[1]) * float(wpercent)))
		resizedImg = baseImage.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
		bigImage.paste(resizedImg, (0, 100*keyCount))
		draw.text((0, 100*keyCount), str(0.0), (255, 255, 255), font=font)

		innerCount = 1 # track iterations in the inner loop

		for innerKey, innerValue in similarities[key].items():
			addImage = Image.open(innerKey)
			wpercent = (basewidth / float(addImage.size[0]))
			hsize = int((float(addImage.size[1]) * float(wpercent)))
			resizedAddImage = addImage.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			bigImage.paste(resizedAddImage, (100*innerCount, 100*keyCount))
			draw.text((100*innerCount, 100*keyCount), str(innerValue), (255, 255, 255), font=font)
			innerCount += 1
		keyCount += 1
		progressThree.update((float(keyCount)/validPics)*100)
	progressThree.finish()
	bigImage.save("sims.jpg")
	bigImage.show()

	# Allow users to specify similarity thresholds, ie. cluster them together if they are above x similarity
	# You really need to sort the dictionaries before the image concatenation

	print "Specify similarity cutoff (0 = identical, 1 = dissimilar) x. Any photo whose similarity value is below x will be relocated or purged."
	threshold = raw_input("Cutoff: ")

	if int(threshold) < 0 or int(threshold) > 1:
		print "Such bounds are illegal!"
	print threshold

	"""

	# Allow users to specify numbers and ranges corresponding to what they want to move
	print "List the numbers and ranges of images that you want to move, separating each entry with a comma. Example: 1-4, 6, 8, 11-15."
	print "Legal photo numbers for your directory range from 1 to " + str(len(sorted_dictionary)-1) + ".\n"
	var = raw_input("List: ")
	splits = var.split(",", 1) # split string by commans
	move = []

	for i in range(len(splits)):
		splits[i] = splits[i].replace(" ", "") # replace spaces in string
		if "-" in splits[i]:
			dashed = splits[i].split("-", 1)
			if not (dashed[0].isdigit() and dashed[1].isdigit()):
				continue
			if int(dashed[0]) > int(dashed[1]):
				temp = dashed[1]
				dashed[1] = dashed[0]
				dashed[0] = temp
			if int(dashed[0]) < 1:
				print str(int(dashed[0])) + " is too puny for our instruments to detect. Raising to min acceptable number...\n"				
				dashed[0] = 1
			if int(dashed[1]) >= len(sorted_dictionary):
				print str(int(dashed[1])) + " is beyond our comprehension. Truncating to max acceptable number...\n"
				dashed[1] = len(sorted_dictionary)-1
			print "Start: " + str(dashed[0])
			print "End: " + str(dashed[1])
			for j in range(int(dashed[0]), int(dashed[1])):
				move.append(int(j))
			move.append(int(dashed[1]))
		else:
			if not splits[i].isdigit():
				continue
			if int(splits[i]) < 1 or int(splits[i]) >= len(sorted_dictionary):
				print str(int(splits[i])) + " is out of orbit. Skipping...\n"
				continue
			move.append(int(splits[i]))
"""