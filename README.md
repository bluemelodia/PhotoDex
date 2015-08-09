|- - - - - - - - - Welcome to PhotoDex Laboratory - - - - - - - - -|

We are a mostly ethical laboratory that specializes in manipulating and mutating directories of photos.<br />
Currently supported experimental procedures are outlined below:<br />
    
    Protocol 'C': 
        [Sub-Protocol 'D']: Generating bar graphs of the n (n <= 10) dominant colors in images and storing
            a record of the dominant color graphs in a user-specified directory. 
        
		Sample Inputs:
			Relative Path to Source Directory: ../Profile_Pictures
			Relative Path to Destination Directory: ../Profile_Pictures_Original
			I choose: C
			Enter 'Q' to query directory, 'D' to calculate dominant colors: D

	[Sub-Protocol 'Q']: Search an directory and rank its images by color similarity to a user-specified
            query image. The ranked images are displayed to the user, who is given the option to specify
            which images they would like to move to a specified destination directory.
	
		Sample Inputs:
			Relative Path to Source Directory: ../Profile_Pictures
			Relative Path to Destination Directory: ../Profile_Pictures_Original
			I choose: C
			Enter 'Q' to query directory, 'D' to calculate dominant colors: Q
			Enter relative path to your query image: ../cero.png
			
    Protocol 'D': Deleting or relocating duplicate or near-duplicate images (coming soon)
    Protocol 'F': Detecting humans and relocating photos that feature them as the subject matter.
		
		Sample Inputs:
			Relative Path to Source Directory: ../Profile_Pictures
			Relative Path to Destination Directory: ../Profile_Pictures_Original
			I choose: F
			Would you like to see each image in a popup window? ('Y'/'N'): Y
			
    Protocol 'S': Shrinking photos according to a specified height or width. A photo expansion option 
        is unavailable due to the extremely high risk of image pixellation and uglification.
    		
		Sample Inputs:
			Relative Path to Source Directory: ../Profile_Pictures_Original
			Relative Path to Destination Directory: ../Profile_Pictures_Original
			I choose: S
			Enter your impossible-to-attain ideal size: 500
			Do you want them short or skinny? ('H' - height/'W' - width): W

    Protocol 'T': Detecting and translating text in photos (coming soon)
    Protocol 'W': Analyzing screenshots of workout machines and generating a report (coming soon)

Research Notes: <br />
Due to limitations in face detection algorithms, Protocol 'F' does not have a 100% accuracy rate.
