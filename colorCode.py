# Created by: Melanie Hsu (bluemelodia)

# A class that handles dominant color calculations in an image. There's an option to create
# and save dominant color bar graphs of all images in a directory - activated by the user 
# adding D as the last command-line argument:
# example: python main.py ../iPhone_Photo_Short C ../Sentient_Beings D

# The second option is querying a directory with a single image, which will find all the 
# images that have similar dominant color schemes. Activated by adding Q as the last argument.
# Additionally, instead of a directory, the fourth command-line argument must be the relative
# path to the image you are using to query
# example: python main.py ../iPhone_Photo_Short C ../cero.png Q

from sklearn.cluster import KMeans
#from skimage.measure import structural_similarity as ssim
import matplotlib.pyplot as pyplot 
import math
import random
import numpy as np
import scipy
import argparse
import cv2
import os
import sys
import operator
import PIL
import re
from PIL import Image
from PIL import ImageFont
from PIL import ImageDraw
import imghdr as I

from progressbar import AnimatedMarker, Bar, BouncingBar, Counter, ETA, \
                        FileTransferSpeed, FormatLabel, Percentage, \
                        ProgressBar, ReverseBar, RotatingMarker, \
                        SimpleProgress, Timer

# count the number of pixels belonging to each cluster
def centroidHist(clt):
	# grab number of clusters; this function returns evenly spaced values within the given interval
	numLabels = np.arange(0, len(np.unique(clt.labels_)) + 1)

	# compute a histogram of the number of pixels assigned to each cluster
	(hist, _) = np.histogram(clt.labels_, bins = numLabels)

	# normalize the histogram so it sums to one
	hist = hist.astype("float")
	hist /= hist.sum()

	return hist

# requires the histogram and list of centroids/cluster centers generated by the k-means algorithm
def plotColors(hist, centroids):
	# initialize bar chart representing the relative frequency of each color
	bar = np.zeros((50, 300, 3), dtype = "uint8") # returns a new array of given shape and type filled with 0s
	startX = 0

	# loop of % of each cluster and the cluster color
	for (percent, color) in zip(hist, centroids):
		# plot relative percentage of each cluster
		endX = startX + (percent * 300)

		# draw the percentage that the current color contributes to the image
		cv2.rectangle(bar, (int(startX), 0), (int(endX), 50), color.astype("uint8").tolist(), -1)
		startX = endX

	# return the bar chart
	return bar

# Calculate Mean Square Error between two images (the sum of the square difference between two images)
# The lower the error, the higher the image similarity
def meanSquareError(A, B):
	# converting to float prevents wrapping
	# subtract the pixels intensities of B from A
	error = np.sum((A.astype("float")-B.astype("float"))**2) 
	error /= float(A.shape[0] * A.shape[1]) # divide sum by number of pixels in the image
	return error

def chi2_distance(histA, histB, eps = 1e-10):
	# compute the chi-squared distance
	d = 0.5 * np.sum([((a - b) ** 2) / (a + b + eps)
		for (a, b) in zip(histA, histB)])

	# return the chi-squared distance
	return d

# finds and saves a bar image of the most dominant colors in a picture in the destination directory 
# the dominant color images are saved in the destination directory of the user's choice
def dominantColors(listDir, directory, destDir):
	# step through all files in directory
	path, dirs, files = os.walk(sys.argv[1]).next()

	# initialize the progress variables
	total = len(files)
	count = 0
	progress = 0

	# initialize the progress bar
	progress = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()

	for imgpath in listDir:
		path = directory + "/" + imgpath

		# update progress and display it to the user
		count += 1

		if I.what(path) != None:
			imagePath = directory + "/" + imgpath

			# load the image nand convert it from BGR to RGB, enabling display with matplotlib
			image = cv2.imread(imagePath)
			image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

			# reshape the NumPy array to a list of RGB pixels
			# img.shape returns a tuple with number of rows, columns, and channels (if in color)
			image = image.reshape((image.shape[0]*image.shape[1], 3))

			# cluster the pixel intensities 
			cluster = KMeans(5)
			cluster.fit(image)

			# build a histogram of clusters, then draw a bar graph 
			# depicting the most dominant colors in the image
			hist = centroidHist(cluster)
			bar = plotColors(hist, cluster.cluster_centers_)
			
			scipy.misc.toimage(bar, cmin=0.0, cmax=None).save(destDir + "/" + imgpath)

			progress.update((float(count)/total)*100)
		else:
			progress.update((float(count)/total)*100)
			continue
	progress.finish()

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

# query a directory of images for images that are similar in color
# for this to work, you must first supply the query image as a commmand-line argument
def queryByColor(imageDir, directory, queryImage):
	# necessary check to see if the image can be used to query
	queryPath = os.path.abspath(queryImage)

	if I.what(queryPath) == None:
		sys.exit("Your image is unfailingly corrupted!")

	# step through all files in directory
	path, dirs, files = os.walk(sys.argv[1]).next()

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
	for imgpath in imageDir:
		path = directory + "/" + imgpath

		# update progress and display it to the user
		count += 1	

		if I.what(path) != None:
			validPics += 1
			imagePath = directory + "/" + imgpath

			otherHist = {}
			otherImg = Image.open(imagePath)
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
			differences[norm] = imagePath
			progress.update((float(count)/total)*100)
		else:
			progress.update((float(count)/total)*100)
			continue
	progress.finish()
	print "\nFinished image similarity calculations.\n"

	# sort the images from most to least similar to query
	sorted_dictionary = sorted(differences.items(), key=operator.itemgetter(0))

	print "Generating rankings...\n"

	# initialize the second progress bar
	progressTwo = ProgressBar(widgets=[Percentage(), Bar()], maxval=100).start()
	counting = 0

	# resize images, then concatenate them into one large image, labeling them by number
    	font = ImageFont.load_default()
    	bigImage = Image.new('RGB', (100*(validPics), 100))
    	draw = ImageDraw.Draw(bigImage)

    	for (i, (value, image)) in enumerate(sorted_dictionary):
    		counting += 1
		basewidth = 100
		img = Image.open(image)
		wpercent = (basewidth / float(img.size[0]))
		hsize = int((float(img.size[1]) * float(wpercent)))
		resizedImg = img.resize((basewidth, hsize), PIL.Image.ANTIALIAS)
    		bigImage.paste(resizedImg, (100*i, 0))
    		draw.text((100*i, 0), str(i), (255, 255, 255), font=font)
    		progressTwo.update((float(counting)/validPics)*100)
    	bigImage.save("rankings.jpg")
	print "\n\nImage stitching complete!\n"

	bigImage.show()
	print "List images that you want to move. Separate each number or range by commas. Example: 1-4, 6, 8, 11-15."
	print "Legal photo numbers range from 1 to " + str(len(sorted_dictionary)-1) + ".\n"
	var = raw_input("List:")
	print ("You chose to move: " + var + "\n")
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
				move.append(j)
			move.append(dashed[1])
		else:
			if not splits[i].isdigit():
				continue
			if int(splits[i]) < 1 or int(splits[i]) >= len(sorted_dictionary):
				print str(int(splits[i])) + " is out of orbit. Skipping...\n"
				continue
			move.append(splits[i])
	print move

	#TODO: let users pick which images to move

