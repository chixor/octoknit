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


print "I dont work, sorry!"
sys.exit()

imgfile = sys.argv[2]

bf = brother.brotherFile(sys.argv[1])


pats = bf.getPatterns()

# find first unused pattern bank
patternbank = 100
for i in range(99):
    bytenum = i*7
    if (bf.getIndexedByte(bytenum) != 0x1):
        print "first unused pattern bank #", i
        patternbank = i
        break

if (patternbank == 100):
    print "sorry, no free banks!"
    exit

# ok got a bank, now lets figure out how big this thing we want to insert is
TheImage = Image.open(imgfile)
TheImage.load()

im_size = TheImage.size
width = im_size[0]
print "width:",width
height = im_size[1]
print "height:", height

# debugging stuff here
x = 0
y = 0

x = width - 1
while x > 0:
    value = TheImage.getpixel((x,y))
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
            break
# debugging stuff done

# create the program entry
progentry = []
progentry.append(0x1)  # is used
progentry.append(0x20)  # no idea what this is but dont make it 0x0
progentry.append( (int(width / 100) << 4) | (int((width%100) / 10) & 0xF) )
progentry.append( (int(width % 10) << 4) | (int(height / 100) & 0xF) )
progentry.append( (int((height % 100)/10) << 4) | (int(height % 10) & 0xF) )

# now we have to pick out a 'program name'
patternnum = 901 # start with 901? i dunno
for pat in pats:
    if (pat["number"] >= patternnum):
        patternnum = pat["number"] + 1

#print patternnum
progentry.append(int(patternnum / 100) & 0xF)
progentry.append( (int((patternnum % 100)/10) << 4) | (int(patternnum % 10) & 0xF) )

print "Program entry: ",map(hex, progentry)

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
        if (value != 0):
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
        print hex(n),
    print


if (len(pattmemnibs) % 2):
    # odd nibbles, buffer to a byte
    pattmemnibs.append(0x0)

print len(pattmemnibs), "nibbles of data"

# turn into bytes
pattmem = []
for i in range (len(pattmemnibs) / 2):
    pattmem.append( pattmemnibs[i*2] | (pattmemnibs[i*2 + 1] << 4))

print map(hex, pattmem)
# whew. 


# now to insert this data into the file 

# where to place the pattern program entry
patternbankptr = patternbank*7

# write the new pattern program
for i in range(7):
    bf.setIndexedByte(patternbankptr+i, progentry[i])


# now we have to figure out the -end- of the last pattern is
endaddr = 0x6df

for p in pats:
    endaddr =  min(p['pattend'], endaddr)
print "top address = ", hex(endaddr)

beginaddr = endaddr - bytesForMemo(height) - len(pattmem) -1
print "end will be at ", hex(beginaddr)

if beginaddr <= 0x2B8:
    print "sorry, this will collide with the pattern entry data!"
    exit

# write the memo and pattern entry from the -end- to the -beginning- (up!)
for i in range(len(memoentry)):
    bf.setIndexedByte(endaddr, 0)
    endaddr -= 1

for i in range(len(pattmem)):
    bf.setIndexedByte(endaddr, pattmem[i])
    endaddr -= 1

# push the data to a file
outfile = open(sys.argv[3], 'wb')

d = bf.getFullData()
outfile.write(d)
outfile.close()
