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

	if (validPics == 0):
		sys.exit("\nNo valid pics in file...abort abort!\n")

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

	print "\nSpecify similarity cutoff between 0 and 1 (0 = identical, 1 = dissimilar)."
	threshold = raw_input("Cutoff: ")

	if float(threshold) < 0 or float(threshold) > 1:
		print "\nSuch bounds are illegal!\n"

	print "\nImage clustering begins...\n"

	# Prepare the clusters array, starting with each image in its own separate cluster
	clusters = {}
	clusterCount = 0
	for key, value in similarities.items():
		clusters[clusterCount] = []
		clusters[clusterCount].append(key)
		clusterCount += 1

	for key, value in similarities.items():
		for innerKey, innerValue in similarities[key].items():
			if (float(innerValue) < float(threshold)):
				for i in range(len(clusters)):
					try:
						if key in clusters[i] and innerKey not in clusters[i]:
							clusters[i].append(innerKey)
							for j in range(len(clusters)):
								if i == j:
									continue
								if innerKey in clusters[j]:
									clusters.pop(j)
									break
					except:
						continue
	
	#find the longest cluster (the cluster with the most number of images in it)
	longest = 0
	for index, group in enumerate(clusters):
		if len(clusters[group]) > longest:
			longest = len(clusters[group])
	
	print "Generating cluster images...\n"
	clusterImage = Image.new('RGB', (100*(longest), 100*(len(clusters))))
	draw = ImageDraw.Draw(clusterImage)
	currentCluster = 0

	progressFour = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	# create an image showing all image clusters
	for index, group in enumerate(clusters):
		currentImage = 0
		for image in clusters[group]:
			basewidth = 100
			baseImage = Image.open(image)
			wpercent = (basewidth / float(baseImage.size[0]))
			hsize = int((float(baseImage.size[1]) * float(wpercent)))
			resizedImg = baseImage.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
			clusterImage.paste(resizedImg, (100*currentImage, 100*currentCluster))
			if currentImage == 0:
				draw.text((100*currentImage, 100*currentCluster), str(group), (255, 255, 255), font=font)
			currentImage += 1
		currentCluster += 1
		progressFour.update((float(currentCluster)/len(clusters))*100)
	clusterImage.save("clusters.jpg")
	clusterImage.show()
	progressFour.finish()

	print "\nFor each cluster, specify which image you wish to keep. Clusters with only one image will be skipped.\n"
	for index, group in enumerate(clusters):
		if len(clusters[group]) < 2:
			continue
		print "Acceptable range for cluster " + str(group) + ": 1-" + str(len(clusters[group]))
		keep = raw_input("Cluster " + str(group) + ": ")
		
		keep = int(keep)-1 # turn it back into comp sci ranges
		if float(keep) >= 0 and float(keep) < len(clusters[group]):
			for i in range(len(clusters[group])):
				if i == keep:
					continue
				else:
					thisGroup = clusters[group]
					if flag == 'M':
						try:
							os.rename(thisGroup[i], destDir + "/" + os.path.basename(thisGroup[i]))
						except:
							continue
					else:
						try: 
							os.remove(os.path.basename(thisGroup[i]))
						except:
							continue