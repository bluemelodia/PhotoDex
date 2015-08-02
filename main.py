import cv2
import os
import sys

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
		print "Sorting color protocol activated..."
	elif sys.argv[2] == 'D':
		print "Activating clone detection algorithm...."
	elif sys.argv[2] == 'F':
		print "Commencing search for human life..."
	else:
		print "CRITICAL ERROR: Your intended classification method is either illegal, highly invasive, or nonexistent!\n"
		print "Please consult the manual for our authorized procedures:"
		print "\t'C' - Dominant colors sorting protocol"
		print "\t'D' - Duplicate image sorting protocol"
		print "\t'F' - Search for human life\n"
		sys.exit()

if __name__ == "__main__": main()