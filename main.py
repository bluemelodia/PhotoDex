# Created by: Melanie Hsu (bluemelodia)

# This class performs the necessary command-line argument checks before launching a sorting protocol.
# Some protocols may require additional, optional command-line arguments.

import cv2
import os
import sys

import faceDetection
import shrinkRay
import colorCode

def main():
	#if len(sys.argv) < 4:
	#	sys.exit("Usage: python main.py <relative path to image directory> <sorting method> <relative path to destination folder>\n"
	#	"example: python main.py ../Profile_Pictures P ../Art")

	print "\n- - - - - Welcome to PhotoDex Laboratory - - - - -\n"
	
	Home = raw_input("Relative Path to Source Directory: ")
	try:
		HomeDirectory = os.listdir(Home)
	except:
		print "A giant tortoise is using your home as her new shell! Please provide the address of an abode you still own...\n"
		sys.exit()

	Dest = raw_input("Relative Path to Destination Directory: ")
	try:
		DestDirectory = os.listdir(Dest)
	except:
		print "An angry octopus has dragged your destination to the bottom of the sea! Such misfortune!\n"
		sys.exit()

	print "Home Sweet Home: " + str(Home)
	print "Final Destination: " + str(Dest)

	print "\nChoose Your Illegal Experiment!\n"
	print "Available Procedures: \n"
	print "\t'C' - Dominant colors sorting protocol"
	print "\t'D' - Duplicate image sorting protocol"
	print "\t'F' - Search for human life - face detection protocol"
	print "\t'S' - Shrink ray"
	print "\t'T' - Text recognition and retrieval protocol"
	print "\t'W' - Generate fitness training report"
	Protocol = raw_input("I choose: ")

	if Protocol == 'C':
		subprotocol = raw_input("Enter 'Q' to query directory, 'D' to calculate dominant colors: ")
		if subprotocol == 'Q':
			queryImage = raw_input("Enter relative path to your query image: ")
			print "Color query protocol activated...\n"
			colorCode.queryByColor(Home, HomeDirectory, queryImage)
		elif subprotocol == 'D':
			print "Dominant colors protocol activated...\n"
			colorCode.dominantColors(Home, HomeDirectory, DestDirectory)
		else:
			print "Sorry, that option was blasted into smithereens with most of the dinosaurs...\n"
			sys.exit()
	elif Protocol == 'D':
		print "Activating clone detection algorithm....\n"
		#TODO: would probably have to save past histograms
	elif Protocol == 'F': # detects the presence of sentient beings (humans and cats)
		if len(sys.argv) < 5:
			sys.exit("Protocol F requires an extra argument, 'Y' - show images in new window, 'N' - the opposite of 'Y'\n")
		if (sys.argv[4] != 'Y' and sys.argv[4] != 'N'):
			print "Maybe is not an answer! Do you want to see the potential humans or not? \n"
			sys.exit()
		print "Commencing search for human...\n"
		faceDetection.cascade()
		faceDetection.detectLife(Home, sys.argv[1], sys.argv[4], sys.argv[3])
	elif Protocol == 'S': # reduces the size of photos
		if len(sys.argv) < 6:
			sys.exit("Protocol S requires two extra arguments, desired height/width and 'H' or 'W' - shrink by height or width\n")
		if (sys.argv[4].isdigit() == False):
			print "You'll have to be more specific about the settings for the shrink ray."
			print "How small is small?\n"
			sys.exit()
		if (sys.argv[5] != 'H' and sys.argv[5] != 'W'):
			print "Wait, do you want them short or skinny? You can't expect me to guess!\n"
			sys.exit()
		print "Busting out the shrink ray...\n"
		shrinkRay.shrinkImages(Home, sys.argv[1], sys.argv[4], sys.argv[5])
	elif Protocol == 'T': # retrieves and translates text in photos
		print "Improving human understanding...\n"
	elif Protocol == 'W': # creates a report based on workout screenshots
		print "Generating training reports...\n"

	print "- - - - - Thank you for visiting PhotoDex Laboratory - - - - -\n"

if __name__ == "__main__": main()