#!/usr/bin/python
import Image
import sys

def getprops():
    x = 0
    y = 0
    im_file = Image.open(file_name)
    im_file.load()
    im_size = im_file.size
    width = im_size[0]
    print "width:",width
    height = im_size[1]
    print "height:", height
    x = width - 1
    while x > 0:
        value = im_file.getpixel((x,y))
        if value:
            sys.stdout.write('* ')
        else:
            sys.stdout.write('  ')
        #sys.stdout.write(str(value))
        x = x-1
        if x == 0: #did we hit the end of the line?
            y = y+1
            x = width - 1
            print " "
            if y == height:
                return
            
def main():
    getprops()
    return

file_name = "./qr_test.bmp"

main()


# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
