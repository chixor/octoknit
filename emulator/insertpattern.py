#!/usr/bin/env python

# Copyright 2009  Steve Conklin 
# steve at conklinhouse dot com
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA  02111-1307, USA.

import sys
import brother
import Image
import array

TheImage = None

##################

def roundeven(val):
    return (val+(val%2))

def roundeight(val):
    if val % 8:
        return val + (8-(val%8))
    else:
        return val

def roundfour(val):
    if val % 4:
        return val + (4-(val%4))
    else:
        return val

def nibblesPerRow(stitches):
    # there are four stitches per nibble
    # each row is nibble aligned
    return(roundfour(stitches)/4)

def bytesPerPattern(stitches, rows):
    nibbs = rows * nibblesPerRow(stitches)
    bytes = roundeven(nibbs)/2
    return bytes

def bytesForMemo(rows):
    bytes = roundeven(rows)/2
    return bytes

##############


version = '1.0'

if len(sys.argv) < 5:
    print 'Usage: %s oldbrotherfile pattern# image.bmp newbrotherfile' % sys.argv[0]
    sys.exit()


bf = brother.brotherFile(sys.argv[1])
pattnum = sys.argv[2]
imgfile = sys.argv[3]


pats = bf.getPatterns()

# ok got a bank, now lets figure out how big this thing we want to insert is
TheImage = Image.open(imgfile)
TheImage.load()

im_size = TheImage.size
width = im_size[0]
print "width:",width
height = im_size[1]
print "height:", height



# find the program entry
thePattern = None

for pat in pats:
    if (int(pat["number"]) == int(pattnum)):
        #print "found it!"
        thePattern = pat
if (thePattern == None):
    print "Pattern #",pattnum,"not found!"
    exit(0)

if (height != thePattern["rows"] or width != thePattern["stitches"]):
    print "Pattern is the wrong size, the BMP is ",height,"x",width,"and the pattern is ",thePattern["rows"], "x", thePattern["stitches"]
    exit(0)

# debugging stuff here
x = 0
y = 0

x = width - 1
while x > 0:
    value = TheImage.getpixel((x,y))
    if value[0] < 100 and value[1] < 100 and value[2] < 100:
        sys.stdout.write('* ')
    else:
        sys.stdout.write('  ')
    #sys.stdout.write(str(value[0]));
    #sys.stdout.write(str(value))
    x = x-1
    if x == 0: #did we hit the end of the line?
        y = y+1
        x = width - 1
        print " "
        if y == height:
            break
# debugging stuff done

# now to make the actual, yknow memo+pattern data

# the memo seems to be always blank. i have no idea really
memoentry = []
for i in range(bytesForMemo(height)):
    memoentry.append(0x0)

# now for actual real live pattern data!
pattmemnibs = []
for r in range(height):
    row = []  # we'll chunk in bits and then put em into nibbles
    for s in range(width):
        value = TheImage.getpixel((width-s-1,height-r-1))
        #if (value != 0):
    	if value[0] < 100 and value[1] < 100 and value[2] < 100:
            row.append(1)
        else:
            row.append(0)
    #print row
    # turn it into nibz
    for s in range(roundfour(width) / 4):
        n = 0
        for nibs in range(4):
            #print "row size = ", len(row), "index = ",s*4+nibs

            if (len(row) == (s*4+nibs)):
                break       # padding!
            
            if (row[s*4 + nibs]):
                n |= 1 << nibs
        pattmemnibs.append(n)
        #print hex(n),


if (len(pattmemnibs) % 2):
    # odd nibbles, buffer to a byte
    pattmemnibs.append(0x0)

#print len(pattmemnibs), "nibbles of data"

# turn into bytes
pattmem = []
for i in range (len(pattmemnibs) / 2):
    pattmem.append( pattmemnibs[i*2] | (pattmemnibs[i*2 + 1] << 4))

#print map(hex, pattmem)
# whew. 


# now to insert this data into the file 

# now we have to figure out the -end- of the last pattern is
endaddr = 0x6df

beginaddr = thePattern["pattend"]
endaddr = beginaddr + bytesForMemo(height) + len(pattmem)
print "beginning will be at ", hex(beginaddr), "end at", hex(endaddr)

# Note - It's note certain that in all cases this collision test is needed. What's happening
# when you write below this address (as the pattern grows downward in memory) in that you begin
# to overwrite the pattern index data that starts at low memory. Since you overwrite the info
# for highest memory numbers first, you may be able to get away with it as long as you don't
# attempt to use higher memories.
# Steve

if beginaddr <= 0x2B8:
    print "sorry, this will collide with the pattern entry data since %s is <= 0x2B8!" % hex(beginaddr)
    #exit

# write the memo and pattern entry from the -end- to the -beginning- (up!)
for i in range(len(memoentry)):
    bf.setIndexedByte(endaddr, 0)
    endaddr -= 1

for i in range(len(pattmem)):
    bf.setIndexedByte(endaddr, pattmem[i])
    endaddr -= 1

# push the data to a file
outfile = open(sys.argv[4], 'wb')

d = bf.getFullData()
outfile.write(d)
outfile.close()
