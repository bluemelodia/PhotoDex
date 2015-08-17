# Created by: Melanie Hsu (bluemelodia)

# This class performs the necessary command-line argument checks before launching a sorting protocol.
# You only need to invoke main.py, the program will ask you for the remaining command-line arguments.

import cv2
import os
import sys
import imghdr

import faceDetection
import shrinkRay
import colorCode
import cloneCrush

def main():
	print "\n- - - - - Welcome to PhotoDex Laboratory - - - - -\n"
	
	Home = raw_input("Relative Path to Source Directory: ")
	try:
		HomeDirectory = os.listdir(Home)
	except:
		sys.exit("\nA giant tortoise is using your home as her new shell! Please provide the address of an abode you still own...\n"
)

	Dest = raw_input("Relative Path to Destination Directory: ")
	try:
		DestDirectory = os.listdir(Dest)
	except:
		sys.exit("\nAn angry octopus has dragged your destination to the bottom of the sea! Such misfortune!\n")

	print "\nChoose Your Illegal Experiment!\n"
	print "Available Procedures: \n"
	print "\t'C' - Dominant colors sorting protocol"
	print "\t'D' - Duplicate image sorting protocol"
	print "\t'F' - Search for human life - face detection protocol"
	print "\t'S' - Shrink ray"
	Protocol = raw_input("I choose: ")

	if Protocol == 'C':
		subprotocol = raw_input("Enter 'Q' to query directory, 'D' to calculate dominant colors: ")
		if subprotocol == 'Q':
			queryImage = raw_input("Enter relative path to your query image: ")
			try:
				os.path.isfile(queryImage)
			except:
				sys.exit("\nYour image couldn't make it through the portal in time..\n")
			if imghdr.what(queryImage) is None:
				sys.exit("\nYour image has met a gruesome fate in a black hole.\n")

			print "\nColor query protocol activated...\n"
			colorCode.queryByColor(Home, HomeDirectory, queryImage, Dest)
		elif subprotocol == 'D':
			print "\nDominant colors protocol activated...\n"
			colorCode.dominantColors(Home, HomeDirectory, Dest)
		else:
			sys.exit("\nSorry, that option was blasted into smithereens with most of the dinosaurs...\n")
	elif Protocol == 'D':
		cloneFate = raw_input("Do you want to move or purge similar images? ('M' - relocate, 'P' - purge): ")
		if cloneFate != 'M' and cloneFate != 'P': 
			sys.exit("\nWe don't have the funding for that!\n")
		print "\nActivating clone detection algorithm...\n"
		cloneCrush.cloneCrusher(Home, HomeDirectory, Dest, cloneFate)
		#TODO: would probably have to save past histograms
	elif Protocol == 'F': # detects the presence of sentient beings (humans and cats)
		showWindow = raw_input("Would you like to see each image in a popup window? ('Y'/'N'): ")
		if showWindow == 'Y' or showWindow == 'N':
			print "\nCommencing search for human life...\n"
			faceDetection.cascade()
			faceDetection.detectLife(Home, HomeDirectory, showWindow, Dest)
		else:
			sys.exit("\nI'm afraid that's not an option...\n")
	elif Protocol == 'S': # reduces the size of photos
		dimension = raw_input("Enter your impossible-to-attain ideal size: ")
		if (dimension.isdigit() == False):
			sys.exit("\nYou'll have to be more specific about the settings for the shrink ray.\n")
		heightOrWeight = raw_input("Do you want them short or skinny? ('H' - height/'W' - width): ")
		if (heightOrWeight != 'H' and heightOrWeight != 'W'):
			sys.exit("\nWe cannot comprehend your choice.\n")
		print "\nBusting out the shrink ray...\n"
		shrinkRay.shrinkImages(Home, HomeDirectory, dimension, heightOrWeight)
	else: 
		print "\nThat's evil even by our standards! We absolutely cannot perform that experiment!\n"

	print "- - - - - Thank you for visiting PhotoDex Laboratory - - - - -\n"

if __name__ == "__main__": main()