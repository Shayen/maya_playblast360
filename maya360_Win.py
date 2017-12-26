import sys, os
import maya.cmds as cmds

modulepath = os.path.dirname(__file__)
if modulepath not in sys.path :
	sys.path.append(modulepath)

# Import modules
import maya360_core as core
reload(core)

mainUI_name  = "SALMayaPlayblast360"
mainUI_title = "SAL Maya Playblast 360"

def _createCamera(*args):
	'''create 360 camera rig at (0,0,0)'''

	cameraRig = cmds.camera( n = "sphericalCamera" )

	cam_left  = cmds.camera( n = "cam_left"  , rotation = [0,90,0])
	cam_front = cmds.camera( n = "cam_front" )
	cam_right = cmds.camera( n = "cam_right" , rotation = [0,-90,0])
	cam_back  = cmds.camera( n = "cam_back"  , rotation = [0,180,0])
	cam_up    = cmds.camera( n = "cam_up"    , rotation = [90,0,0])
	cam_down  = cmds.camera( n = "cam_down"  , rotation = [-90,0,0])

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

	# Query data
	destPath 	= cmds.textField( "destDir_textField"	, q=True, tx = True )
	filename 	= cmds.textField("playblastName_textField", q=True, tx=True)
	startFrame 	= cmds.intField ( "startFrame_intField"	, q=True, v  = True )
	endFrame 	= cmds.intField ( "endFrame_intField"	, q=True, v  = True )
	squareSize	= cmds.intField ( "squareSize_intField"	, q=True, v  = True )

	# set OptionVar
	cmds.optionVar(sv=("SALPlayblastDir", destPath))

	if cmds.objExists("sphericalCamera_grp") and len(cmds.listRelatives("sphericalCamera_grp")):
		cam_shapes = [cmds.listRelatives(camera)[0] for camera in cmds.listRelatives("sphericalCamera_grp")]
	else:
		print ( "Camera rig not found." )
		cmds.confirmDialog(m = "Camera rig not found.")
		return False

	# Setup progressBar
	gMainProgressBar = maya.mel.eval('$tmp = $gMainProgressBar');
	cmds.progressBar( 	gMainProgressBar,
						edit=True,
						beginProgress=True,
						isInterruptable=True,
						status='Example Calculation ...',
						maxValue=endFrame )

	cmds.progressBar(gMainProgressBar, edit=True, step=1,status='Example Calculation ...')

	# Setup viewport
	cmds.modelEditor("modelPanel4", e=True, allObjects=False)
	cmds.modelEditor("modelPanel4", e=True, polymeshes=True, pluginObjects = ["gpuCacheDisplayFilter",True])

	# Playblast
	for frame in range(startFrame, endFrame+1):

		print( "_________________" )
		print( "Frame : %s/%s" %(frame, endFrame) )

		for camera in cam_shapes:

			tmp_filename = _getTempImgNameFromCamera(cameraname = camera)

			cmds.lookThru (camera)
			cmds.refresh()

			cmds.playblast(	format 		= "image",
							frame 		= frame,
							wh 			= (squareSize,squareSize),
							percent 	= 100,
							quality 	= 100,
							completeFilename 	= destPath + '/' + tmp_filename,
							compression = "jpg",
							v= False)

		# Combine image
		out_filename = filename.replace("####", "%04d"%frame)
		result = core.createSpherical( 	left 		= destPath + '/' + "tmp_left.jpg",
										front 		= destPath + '/' + "tmp_front.jpg",
										right 		= destPath + '/' + "tmp_right.jpg",
										back 		= destPath + '/' + "tmp_back.jpg",
										top 		= destPath + '/' + "tmp_up.jpg",
										bottom 		= destPath + '/' + "tmp_down.jpg",
										in_widht  	= squareSize, 
										in_height 	= squareSize, 
										output_path = destPath + '/' + out_filename )

		# Remove temp file
		tmp_files = [	destPath + '/' + "tmp_left.jpg",
						destPath + '/' + "tmp_front.jpg",
						destPath + '/' + "tmp_right.jpg",
						destPath + '/' + "tmp_back.jpg",
						destPath + '/' + "tmp_up.jpg",
						destPath + '/' + "tmp_down.jpg" ]

		_deleteTempFiles(tmp_files)

		if cmds.progressBar(gMainProgressBar, query=True, isCancelled=True ) or not result  :
			# Set viewport back
			cmds.modelEditor("modelPanel4", e=True, allObjects=True)
			_deleteTempFiles(tmp_files)
			cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)
			return

		cmds.progressBar(gMainProgressBar, edit=True, step=1)

	# Set viewport back
	cmds.modelEditor("modelPanel4", e=True, allObjects=True)
	cmds.progressBar(gMainProgressBar, edit=True, endProgress=True)

def _deleteTempFiles(tempFiles):
	'''Delete temp files'''
	for file in tempFiles :
		if os.path.exists(file) :
			os.remove(file)

def _setDestDir(*args):
	'''set Destination folder'''
	playBlastDir = cmds.fileDialog2(fileMode = 3, dialogStyle=2)

	cmds.textField("destDir_textField", e=True, tx = playBlastDir[0])


def _getTempImgNameFromCamera( cameraname ):
	''' Generate image temp name from camera name '''

	if "cam_left" in cameraname :
		return "tmp_left.jpg"

	elif "cam_front" in cameraname :
		return "tmp_front.jpg"

	elif "cam_right" in cameraname :
		return "tmp_right.jpg"

	elif "cam_back" in cameraname :
		return "tmp_back.jpg"

	elif "cam_up" in cameraname :
		return "tmp_up.jpg"

	elif "cam_down" in cameraname :
		return "tmp_down.jpg"


def showUI():
	'''show main window'''
	clearUI()

	# Get playblast path
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
	cmds.intField("squareSize_intField",v=960)
	cmds.setParent("..")

	cmds.separator(h=10)

	cmds.button(l="Render playblast", h=40, c= _renderVR)
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