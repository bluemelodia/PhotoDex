import cv2
import os
import sys

def main():
	if len(sys.argv) < 4:
		sys.exit("Usage: python main.py <image directory name> <sorting method> <path to destination folder>\n")

	print "\n- - - - - - Welcome to PhotoDex - - - - - -\n"
	print "\tImage Directory: " + sys.argv[1]
	print "\tSorting Method: " + sys.argv[2]
	print "\tDestination Directory: " + sys.argv[3] + "\n"

	#Home = os.listdir(sys.argv[1])

if __name__ == "__main__": main()