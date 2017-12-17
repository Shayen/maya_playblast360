import sys, os
import maya.cmds as cmds

# Import modules
try:
	from src import combine
except ImportError :
	modulePath = os.path.dirname(__file__)
	print modulePath
	sys.path.append(modulePath)
	sys.path.append("C:\Python27\Lib\site-packages")

	from src import combine

mainUI_name  = "SALMayaPlayblast360"
mainUI_title = "SAL Maya Playblast 360"

def _createCamera(*args):
	'''create 360 camera rig at (0,0,0)'''

	cameraRig = cmds.camera( n = "sphericalCamera" )

	cam_left  = cmds.camera( n = "camera_left" )
	cam_front = cmds.camera( n = "cam_front" )
	cam_right = cmds.camera( n = "cam_right" )
	cam_back  = cmds.camera( n = "cam_back" )
	cam_up    = cmds.camera( n = "cam_up" )
	cam_down  = cmds.camera( n = "cam_down" )

	# Setup each camera
	for camera, cameraShape in [cam_left, cam_front, cam_right, cam_back, cam_up, cam_down]:
		# Set film gate to 35mm Academy
		cmds.setAttr( cameraShape + '.horizontalFilmAperture', 0.864 )
		cmds.setAttr( cameraShape + '.verticalFilmAperture', 0.630  )

		# Set view angle to 90 degree
		cmds.setAttr( cameraShape + '.focalLength', 10.973  )
		cmds.setAttr( cameraShape + '.overscan', 1.0  )

	c_cameraGrp = cmds.group( 	cam_left, cam_front, cam_right, cam_right, cam_back, cam_up, cam_down,
								name = "sphericalCamera_grp", 
								parent = cameraRig[0])

	cmds.hide(c_cameraGrp)

	print ("360 camera was create.")

def _renderVR(*args):
	'''Render playblast to vr'''

	currentPath = cmds.textField("destDir_textField", q=True, tx = currentPath)

	# set OptionVar
	cmds.optionVar(sv=("SALPlayblastDir", currentPath))

def _setDestDir(*args):
	'''set Destination folder'''
	playBlastDir = cmds.fileDialog2(fileMode = 3, dialogStyle=2)

	cmds.textField("destDir_textField", e=True, tx = playBlastDir[0])

def _playblast(camera, start, stop, outputPath, fileName):
	'''
	Playblast
	From : playblast  -format image -filename "playblast" -sequenceTime 0 -clearCache 1 -viewer 1 -showOrnaments 1 -fp 4 -percent 50 -compression "jpg" -quality 80;
	'''

	cmds.playBlast(	format = "image",
					fp = 4,
					percent = 100,
					quality = 100,
					compression = "jpg")

def showUI():
	'''show main window'''
	clearUI()

	# Get playblast path
	# currentPath = cmds.getAttr("defaultRenderGlobals.imageFilePrefix")
	if cmds.optionVar( exists = 'SALPlayblastDir' ) :
		currentPath = cmds.optionVar( q = 'SALPlayblastDir' )
	else :
		currentPath = ""

	# Get start frame
	startFrame = cmds.getAttr("defaultRenderGlobals.startFrame")

	# Get End frame
	endFrame = cmds.getAttr("defaultRenderGlobals.endFrame")

	cmds.window(mainUI_name, title = mainUI_title)
	cmds.columnLayout(adj=True)

	cmds.columnLayout(adj=True)
	cmds.text(l="\nCreate 360 camera", align = "left")
	cmds.button(l="Create camera", c=_createCamera)
	cmds.separator(h=10)
	cmds.setParent("..")

	cmds.columnLayout(adj=True)
	cmds.text(l="Destination path :", align = "left")

	cmds.rowLayout(nc=2,adj=1)
	cmds.textField("destDir_textField", tx = currentPath)
	cmds.button(l="...", c=_setDestDir, w = 40 )
	cmds.setParent("..")

	cmds.rowLayout(nc=2,adj=2)
	cmds.text("File name :")
	cmds.textField("playblastName_textField", tx = "playBlast.####.jpg")
	cmds.setParent("..")

	cmds.rowLayout(nc=4, ad2 = 40, ad4 = 40)
	cmds.text("Start : ", align = "right")
	cmds.intField("startFrame_intField", v = startFrame)
	cmds.text("End : ", align = "right")
	cmds.intField("endFrame_intField", v = endFrame)
	cmds.setParent("..")

	cmds.rowLayout(nc=2)
	cmds.text("Square size : ")
	cmds.intField(v=960)
	cmds.setParent("..")

	cmds.separator(h=10)

	cmds.button(l="Render playblast", h=40)
	cmds.setParent("..")

	cmds.columnLayout(adj=True)
	cmds.text("\n")
	cmds.text("by Sirasit Sawetprom")
	cmds.text("Version : 0.1b")
	cmds.setParent("..")

	cmds.showWindow(mainUI_name)

	# Adjust window size
	cmds.window(mainUI_name, e = True, w = 400 )

def clearUI():
	'''Clear ui'''
	if cmds.window(mainUI_name,q=True, exists=True) :
		cmds.deleteUI(mainUI_name)
		clearUI()

if __name__ == '__main__':
	showUI()