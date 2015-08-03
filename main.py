# Created by: Melanie Hsu (bluemelodia)

# This class performs the necessary command-line argument checks before launching a sorting protocol.
# Some protocols may require additional, optional command-line arguments.

import cv2
import os
import sys

import faceDetection
import shrinkRay

def main():
	if len(sys.argv) < 4:
		sys.exit("Usage: python main.py <relative path to image directory> <sorting method> <relative path to destination folder>\n"
		"example: python main.py ../Profile_Pictures P ../Art")

	print "\n- - - - - Welcome to PhotoDex Laboratory - - - - -\n"
	print "\tImage Directory: " + sys.argv[1]
	print "\tSorting Method: " + sys.argv[2]
	print "\tDestination Directory: " + sys.argv[3] + "\n"

	try:
		Home = os.listdir(sys.argv[1])
	except:
		print "ERROR: Your home directory is not where you say it is!"
		print "Your integrity as a scientist has been called into question!\n"
		sys.exit()

	try:
		Dest = os.listdir(sys.argv[3])
	except:
		print "ALERT: Your destination directory has fled the premises!"
		print "We shall wait patiently while you attempt to recapture it.\n"
		sys.exit()

	if sys.argv[2] == 'C':
		print "Sorting color protocol activated...\n"
	elif sys.argv[2] == 'D':
		print "Activating clone detection algorithm....\n"
	elif sys.argv[2] == 'F': # detects the presence of sentient beings (humans and cats)
		if (sys.argv[4] != 'Y' and sys.argv[4] != 'N'):
			print "Maybe is not an answer! Do you want to see the potential humans or not? \n"
			sys.exit()
		print "Commencing search for human...\n"
		faceDetection.cascade()
		faceDetection.detectLife(Home, sys.argv[1], sys.argv[4], sys.argv[3])
	elif sys.argv[2] == 'S': # reduces the size of photos
		if (sys.argv[4].isdigit() == False):
			print "You'll have to be more specific about the settings for the shrink ray."
			print "How small is small?\n"
			sys.exit()
		if (sys.argv[5] != 'H' and sys.argv[5] != 'W'):
			print "Wait, do you want them short or skinny? You can't expect me to guess!\n"
			sys.exit()
		print "Busting out the shrink ray...\n"
		shrinkRay.shrinkImages(Home, sys.argv[1], sys.argv[4], sys.argv[5])
	elif sys.argv[2] == 'T': # retrieves and translates text in photos
		print "Improving human understanding...\n"
	elif sys.argv[2] == 'W': # creates a report based on workout screenshots
		print "Generating training reports...\n"
	else:
		print "CRITICAL ERROR: Your intended classification method is either illegal, highly invasive, or nonexistent!\n"
		print "Please consult the manual for our authorized procedures:"
		print "\t'C' - Dominant colors sorting protocol"
		print "\t'D' - Duplicate image sorting protocol"
		print "\t'F' - Search for human life - face detection protocol"
		print "\t'S' - Shrink ray\n"
		print "\t'T' - Text recognition and retrieval protocol\n"
		print "\t'W' - Generate fitness training report"
		sys.exit()

if __name__ == "__main__": main()