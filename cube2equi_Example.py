from PIL import Image
from src.cube2equi import find_corresponding_pixel


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
            # print ("(%d,%d) >> (%d,%d)")%(xcoord, ycoord ,corrx ,corry)
        print str(round((float(ycoord)/float(h))*100, 2)) + '%'


    outimg.save(outfile, 'PNG')

input_path = "C:/Users/siras/Desktop/test_playblast/outPut_API.jpg"
outputPath = "C:/Users/siras/Desktop/test_playblast/result_gg.jpg"
convert_img(infile = input_path, outfile = outputPath)