# Combine multiple images into one.
#
# To install the Pillow module on Mac OS X:
#
# $ xcode-select --install
# $ brew install libtiff libjpeg webp little-cms2
# $ pip install Pillow
#

# Folk from : https://gist.github.com/glombard/7cd166e311992a828675

from __future__ import print_function
import os

from PIL import Image

'''
files = [
	'~/Downloads/1.jpg',
	'~/Downloads/2.jpg',
	'~/Downloads/3.jpg',
	'~/Downloads/4.jpg']
'''

def combineToCube( front, back, left, right, up, down, outputPath, outputScale = (3840,2880) ):

	if len(imageList) != 6 :
		return False

	result = Image.new("RGB", outputScale)
	'''
	for index, file in enumerate(files):
		path = os.path.expanduser(file)
		img = Image.open(path)
		img.thumbnail((400, 400), Image.ANTIALIAS)
		x = index // 2 * 400
		y = index % 2 * 400
		w, h = img.size
		print('pos {0},{1} size {2},{3}'.format(x, y, w, h))
		result.paste(img, (x, y, x + w, y + h))
	'''
	# Define conner
	# center line
	# h_Line = (outputScale[1] // 3 ) + ((outputScale[1] / 3 ) // 2 )
	v_Line = (outputScale[0] / 4 )

	# past center line
	for index, file in enumerate( [left, front, right, back] ):
		img = Image.open(file)

		# define position
		c_left  = v_Line
		c_upper = ((outputScale[0] / 4 ) * (index) ) 

		result.paste(img, (c_upper, c_left))

	# Up ========================================
	# Load image
	img = Image.open(up)

	# define position
	c_left  = ( outputScale[1] / 3 ) * 0 
	c_upper = ( outputScale[0] / 4 )  

	result.paste(img, (c_upper, c_left))

	# Down ========================================
	# Load image
	img = Image.open(down)

	# define position
	c_left  = (( outputScale[1] / 3 ) * 2)
	c_upper = ( outputScale[0] / 4 )

	result.paste(img, (c_upper, c_left))

	result.save( os.path.expanduser( outputPath ) )

if __name__ == '__main__':
	imageList 	= [	"C:/Users/siras/Desktop/test_playblast/back.jpg",
									"C:/Users/siras/Desktop/test_playblast/down.jpg",
									"C:/Users/siras/Desktop/test_playblast/front.jpg",
									"C:/Users/siras/Desktop/test_playblast/left.jpg",
									"C:/Users/siras/Desktop/test_playblast/right.jpg",
									"C:/Users/siras/Desktop/test_playblast/up.jpg",]

	outputPath 	=   "C:/Users/siras/Desktop/test_playblast/result.jpg"

	combineToCube(	front = imageList[2], 
									back 	= imageList[0], 
									left 	= imageList[3], 
									right = imageList[4], 
									up 		= imageList[5], 
									down 	= imageList[1], 
									outputPath = outputPath )