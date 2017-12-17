from PIL import Image
from src.cube2equi import find_corresponding_pixel

import threading

def convert_img(infile, outfile):

    print("processing ...")
    inimg = Image.open(infile)

    wo, ho = inimg.size

    # Calculate height and width of output image, and size of each square face
    h = wo/3
    w = 2*h
    n = ho/3

    # Create new image with width w, and height h
    outimg = Image.new('RGB', (w, h))

    # For each pixel in output image find colour value from input image
    for ycoord in range(0, h):
        for xcoord in range(0, w):
            corrx, corry = find_corresponding_pixel(xcoord, ycoord, w, h, n)

            outimg.putpixel((xcoord, ycoord), inimg.getpixel((corrx, corry)))
        # Print progress percentage
        percent = round((float(ycoord)/float(h))*100, 2)
        if (percent % 10) == 0 :
        	print percent


    outimg.save(outfile, 'PNG')
    print ("save image : " + outfile)

input_path = "C:/Users/siras/Desktop/test_playblast/result.jpg"
outputPath = [	"C:/Users/siras/Desktop/test_playblast/result_o.jpg",
				"C:/Users/siras/Desktop/test_playblast/result_o2.jpg",
				"C:/Users/siras/Desktop/test_playblast/result_o3.jpg"]

thread = []				
for img in outputPath : 

	t = threading.Thread( target = convert_img, args = (input_path, img))
	# convert_img(infile = input_path, outfile = outputPath)
	thread.append(t)
	t.start()