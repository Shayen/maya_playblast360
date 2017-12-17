#!D:/Program Files/Autodesk/Maya2016/bin/mayapy.exe
# TestMayaIImage.py

import os,sys

from src.cube2equi import find_corresponding_pixel

import maya.standalone
maya.standalone.initialize(name='python')
import maya.cmds as cmds
import maya.OpenMaya as om 

class MayaImage :
	"""
	The main class, needs to be constructed with a filename
	
	REF : https://jonmacey.blogspot.com/2011/04/using-maya-mscriptutil-class-in-python.html
	"""

	def __init__( self ) :
		""" constructor pass in the name of the file to load (absolute file name with path) """

		# create an MImage object
		self.image = om.MImage()

		# finally create an empty script util and a pointer to the function
		# getUcharArrayItem function for speed
		scriptUtil = om.MScriptUtil()
		self.getUcharArrayItem = scriptUtil.getUcharArrayItem
		self.setUcharArray = scriptUtil.setUcharArray

	def readFromFile(self,filepath):
		"""Load image data"""
		# read from file MImage should handle errors for us so no need to check
		self.image.readFromFile(filepath)

		widthPtr, heightPtr = self._setupWidthHeight( w = 0, h = 0 )

		# now we call the MImage getSize method which needs the params passed as pointers
		# as it uses a pass by reference
		self.image.getSize( widthPtr, heightPtr )

		# once we get these values we need to convert them to int so use the helpers
		self.m_width  = self.scriptUtilWidth.getUint(widthPtr)
		self.m_height = self.scriptUtilHeight.getUint(heightPtr)

		# now we grab the pixel data and store
		self.charPixelPtr = self.image.pixels()

		# query to see if it's an RGB or RGBA image, this will be True or False
		self.m_hasAlpha = self.image.isRGBA()

		# if we are doing RGB we step into the image array in 3's
		# data is always packed as RGBA even if no alpha present
		self.imgStep = 4

	def create(self,w,h):
		"""Create a new MImage object."""

		widthPtr, heightPtr = self._setupWidthHeight( w = w, h = h )

		# once we get these values we need to convert them to int so use the helpers
		self.m_width  = self.scriptUtilWidth.getUint ( widthPtr  )
		self.m_height = self.scriptUtilHeight.getUint( heightPtr )

		self.image.create(	w, h, 4, self.image.kByte)

		self.charPixelPtr = self.image.pixels()

	def _setupWidthHeight(self,w,h):
		# as the MImage class is a wrapper to the C++ module we need to access data
		# as pointers, to do this use the MScritUtil helpers
		self.scriptUtilWidth  = om.MScriptUtil()
		self.scriptUtilHeight = om.MScriptUtil()

		# first we create a pointer to an unsigned in for width and height
		widthPtr  = self.scriptUtilWidth.asUintPtr()
		heightPtr = self.scriptUtilHeight.asUintPtr()

		# now we set the values to 0 for each
		self.scriptUtilWidth.setUint( widthPtr, w )
		self.scriptUtilHeight.setUint( heightPtr, h )

		# print self.scriptUtilWidth

		return widthPtr, heightPtr
  
	def width(self) :
		""" return the width of the image """
		return self.m_width
	 
	def height(self) :
		""" return the height of the image """
		return self.m_height
	 
	def hasAlpha(self) :
		""" return True is the image has an Alpha channel """
		return self.m_hasAlpha

	def getPixel(self,x,y) :
		""" get the pixel data at x,y and return a 3/4 tuple depending upon type """
		# check the bounds to make sure we are in the correct area
		if x < 0 or x > self.m_width :
			print "error x out of bounds\n"
			return
		if y < 0 or y > self.m_height :
			print "error y our of bounds\n"
			return
		# now calculate the index into the 1D array of data
		index=(y*self.m_width*4)+x*4
		# grab the pixels
		red 	= self.getUcharArrayItem(self.charPixelPtr,index)
		green 	= self.getUcharArrayItem(self.charPixelPtr,index+1)
		blue 	= self.getUcharArrayItem(self.charPixelPtr,index+2)
		alpha 	= self.getUcharArrayItem(self.charPixelPtr,index+3)
		return (red,green,blue,alpha)

	def setPixel(self, x, y, color = [255,255,255] ):
		"""
		set pixel data to new Image
		"""

		index = ( y * (self.m_width*4) ) + x * 4 

		# setIntArray
		self.setUcharArray ( self.charPixelPtr, index  , color[0] )
		self.setUcharArray ( self.charPixelPtr, index+1, color[1] )
		self.setUcharArray ( self.charPixelPtr, index+2, color[2] )
		self.setUcharArray ( self.charPixelPtr, index+3, 255 )

	def saveToFile(self, path, ext = "jpg"):
		"""Save to file"""
		self.image.writeToFile( path, ext )
		return path

def createSpherical( left, front, right, back, top, bottom, in_widht, in_height, output_path ):
	"""
	Combine six image together 

	1). Create cube map
	2). Convert cube map to equi map

			______
		   |      |
		   | top  |
		   |      |
	------------------------------
	|      |      |      |       |
	| left | front| right| back  |
	|      |      |      |       |
	------------------------------
		   |      |
		   |Buttom|
		   |      |
		   --------
	"""

	cube_widht  = in_widht  * 4
	cube_height = in_height * 3

	# Set output image object
	cube_img = MayaImage()
	cube_img.create (w = cube_widht, h = cube_height)

	print ("Combine Cube map :")

	# 1). Combine CUBE Image
	for index, imageFile in enumerate([ left, front, right, back, top, bottom ]) :

		# Check file exists
		if not os.path.exists(imageFile):
			break

		print ("\t-" + imageFile)

		# Set Offset
		if index   == 0:
			# Left
			x_offset = in_widht * 0
			y_offset = in_height

		elif index == 1:
			# Front
			x_offset = in_widht * 1
			y_offset = in_height

		elif index == 2 :
			# Right
			x_offset = in_widht * 2
			y_offset = in_height

		elif index == 3 :
			# Back
			x_offset = in_widht * 3
			y_offset = in_height

		elif index == 5 :
			# Buttom
			x_offset = in_widht
			y_offset = in_height * 0

		elif index == 4 :
			# Top
			x_offset = in_widht
			y_offset = in_height * 2


		img = MayaImage()
		img.readFromFile(filepath = imageFile)

		for y in range (0,img.height()) :

			# print ("Row : %d")%y

			for x in range(0,img.width()) :
				r,g,b,a = img.getPixel(x,y)

				cube_img.setPixel( x = x + x_offset, y = y + y_offset, color = [r,g,b])

	cube_img.saveToFile(path = "C:/Users/siras/Desktop/test_playblast/outPut_API.jpg" )

	# return

	# 2). Create Spherical
	o_img = MayaImage()

	out_widht  = in_widht  * 4
	out_height = in_height * 2

	wo = cube_img.width()
	ho = cube_img.height()

	# Calculate height and width of output image, and size of each square face
	h = in_widht
	w = in_widht *2
	n = in_widht

	o_img.create(w = w, h = h)

	for y in range (0,h) :

		# print ("Row : %d")%y

		for x in range(0,w) :
			

			corrx, corry = find_corresponding_pixel(i = x, j = y, 
													w = w, h = h, 
													n = n)

			r,g,b,a = cube_img.getPixel(int(corrx),int(corry))

			# print ("(%d,%d) >> (%d,%d)")%(x, y ,corrx ,corry)

			o_img.setPixel( x = x, y = y, color = [r,g,b])

			# print((corrx, corry))

		percent = round((float(y)/float(h))*100, 2)
		if percent % 1 == 0 :
			print ("Percent : %.2f/100"%(percent))
			o_img.saveToFile(path = output_path )

	o_img.saveToFile(path = output_path )

if __name__ == '__main__':
	
	imageList 	= [	"C:/Users/siras/Desktop/test_playblast/back.jpg",
					"C:/Users/siras/Desktop/test_playblast/down.jpg",
					"C:/Users/siras/Desktop/test_playblast/front.jpg",
					"C:/Users/siras/Desktop/test_playblast/left.jpg",
					"C:/Users/siras/Desktop/test_playblast/right.jpg",
					"C:/Users/siras/Desktop/test_playblast/up.jpg",]

	createSpherical( 	left 	= imageList[3],
						front 	= imageList[2], 
						right 	= imageList[4], 
						back 	= imageList[0], 
						top 	= imageList[5], 
						bottom 	= imageList[1], 
						in_widht  = 960, 
						in_height = 960, 
						output_path = "C:/Users/siras/Desktop/test_playblast/result_gg.jpg")