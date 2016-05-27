import os
import sys
from PIL import Image, ImageStat

def compare_images(image1, image2):
    out1 = list(image1.getdata())
    out2 = list(image2.getdata())

    if out1 == out2:
        return True
    else:
        return False

def compare_images_b(image1,image2):
        out1 = ImageStat.Stat(image1)
        out2 = ImageStat.Stat(image2)

        if (out1.rms == out2.rms) and (out1.sum == out2.sum) and (out1.var == out2.var):
            return True
        else:
            return False

def single_image_test():
    testimage1 = "/home/jmccarth/public_html/campus-map-demo/tiles/default/0/0/0.png"
    testimage2 = "/home/jmccarth/public_html/campus-map-demo/tiles/hc/0/0/0.png"
    t1 = Image.open(testimage1)
    t2 = Image.open(testimage2)
    print compare_images(t1, t2)


tileset_1 = """/home/jmccarth/public_html/campus-map-demo/tiles/default"""
tileset_2 = """/home/jmccarth/public_html/campus-map-demo/new-tiles/default"""
outfilename = """/home/jmccarth/public_html/campus-map-demo/tiles/compare.txt"""
target = open(outfilename,'w')
mismatches = []
tile_count = 0
compared_count = 0

for dirName, subdirList, fileList in os.walk(tileset_1):
    for fname in fileList:
        if ".png" in fname:
            tile_count = tile_count + 1
print ('number of tiles:' + str(tile_count))

for dirName, subdirList, fileList in os.walk(tileset_1):
    for fname in fileList:
        if ".png" in fname:
            compared_count = compared_count + 1
            image_1_path = dirName + "/" + fname
            image_2_path_end = "/".join(image_1_path.split("/")[-3:])
            image_2_path = tileset_2 + "/" + image_2_path_end
            try:
                image1 = Image.open(image_1_path)
                image2 = Image.open(image_2_path)
            except IOError as err:
                print("IO Error: %s" % err)
            else:
                if not(compare_images(image1,image2)):
                    print ("\rComparing tile # %i of %i. Different." % (compared_count, tile_count) )
                    mismatch_file = "/".join(image_1_path.split("/")[-3:])
                    target.write("Diff:" + mismatch_file + "\n")
                    mismatches.append(mismatch_file)
                else:
                    print ("\rComparing tile # %i of %i. Same" % (compared_count, tile_count) )

target.close()
