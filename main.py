import cv2
import os
import sys

def main():
	if len(sys.argv) < 4:
		sys.exit("Usage: python main.py <image directory name> <sorting method> <path to destination folder>\n"
		"example: python main.py ../Profile_Pictures P ../Art")

	print "\n- - - - - - Welcome to PhotoDex - - - - - -\n"
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

	if sys.argv[2] == 'D':
		print "Duplicate sorting activated."
	elif sys.argv[2] == 'C':
		print "Color sorting activated."
	else:
		print "CRITICAL ERROR: Your intended classification method is either illegal, highly invasive, or nonexistent!\n"
		print "Please consult the manual for our authorized procedures:"
		print "\t'D' - Move image duplicates"
		print "\t'C' - Classify images by color\n"
		sys.exit()

if __name__ == "__main__": main()