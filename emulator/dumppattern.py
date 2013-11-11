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

DEBUG = 0

##########

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

if len(sys.argv) < 2:
    print 'Usage: %s file [patternnum]' % sys.argv[0]
    print 'Dumps user programs (901-999) from brother data files'
    sys.exit()

if len(sys.argv) == 3:
    patt = int(sys.argv[2])
else:
    patt = 0

bf = brother.brotherFile(sys.argv[1])

if patt == 0:
    pats = bf.getPatterns()
    print 'Pattern   Stitches   Rows'
    for pat in pats:
        print '  %3d       %3d      %3d' % (pat["number"], pat["stitches"], pat["rows"])

    if DEBUG:
        print "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"
        print "Data file"
        print "-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+-+"

        # first dump the 99 'pattern id' blocks
        for i in range(99):
            print "program entry",i
            # each block is 7 bytes
            bytenum = i*7

            pattused = bf.getIndexedByte(bytenum)
            print "\t",hex(bytenum),": ",hex(pattused),
            if (pattused == 1):
                print "\t(used)"
            else:
                print "\t(unused)"
                #print "\t-skipped-"
                #continue
            bytenum += 1

            unk1 = bf.getIndexedByte(bytenum)
            print "\t",hex(bytenum),": ",hex(unk1),"\t(unknown)"
            bytenum += 1

            rows100 =  bf.getIndexedByte(bytenum)
            print "\t",hex(bytenum),": ",hex(rows100),"\t(rows = ", (rows100 >> 4)*100, " + ", (rows100 & 0xF)*10
            bytenum += 1

            rows1 =  bf.getIndexedByte(bytenum)
            print "\t",hex(bytenum),": ",hex(rows1),"\t\t+ ", (rows1 >> 4), " stiches = ", (rows1 & 0xF)*100,"+"
            bytenum += 1

            stitches10 =  bf.getIndexedByte(bytenum)
            print "\t",hex(bytenum),": ",hex(stitches10),"\t\t+ ", (stitches10 >> 4)*10, " +", (stitches10 & 0xF),")"
            bytenum += 1

            prog100 = bf.getIndexedByte(bytenum)
            print "\t",hex(bytenum),": ",hex(prog100),"\t(unknown , prog# = ", (prog100&0xF) * 100,"+"
            bytenum += 1

            prog10 = bf.getIndexedByte(bytenum)
            print "\t",hex(bytenum),": ",hex(prog10),"\t\t + ", (prog10>>4) * 10,"+",(prog10&0xF),")"
            bytenum += 1

        print "============================================"
        print "Program memory grows -up-"
        # now we're onto data data

        # dump the first program
        pointer = 0x76DF      # this is the 'bottom' of the memory
        for i in range(99):
            # of course, not all patterns will get dumped
            pattused = bf.getIndexedByte(i*7)
            if (pattused != 1):
                # :(
                break
            # otherwise its a valid pattern
            print "pattern bank #", i
            # calc pattern size
            rows100 =  bf.getIndexedByte(i*7 + 2)
            rows1 =  bf.getIndexedByte(i*7 + 3)
            stitches10 =  bf.getIndexedByte(i*7 + 4)

            rows = (rows100 >> 4)*100 + (rows100 & 0xF)*10 + (rows1 >> 4);
            stitches = (rows1 & 0xF)*100 + (stitches10 >> 4)*10 + (stitches10 & 0xF)
            print "rows = ", rows, "stitches = ", stitches
#        print "total nibs per row = ", nibblesPerRow(stitches)


            # dump the memo data
            print "memo length =",bytesForMemo(rows)
            for i in range (bytesForMemo(rows)):
                b = pointer - i
                print "\t",hex(b),": ",hex(bf.getIndexedByte(b))
            pointer -= bytesForMemo(rows)

            print "pattern length = ", bytesPerPattern(stitches, rows)
            for i in range (bytesPerPattern(stitches, rows)):
                b = pointer - i
                print "\t",hex(b),": ",hex(bf.getIndexedByte(b)),
                for j in range(8):
                    if (bf.getIndexedByte(b) & (1<<j)):
                        print "*",
                    else:
                        print " ",
                print ""

            # print it out in nibbles per row?
            for row in range(rows):
                for nibs in range(nibblesPerRow(stitches)):
                    n = bf.getIndexedNibble(pointer, nibblesPerRow(stitches)*row + nibs)
                    print hex(n),
                    for j in range(8):
                        if (n & (1<<j)):
                            print "*",
                        else:
                            print " ",
                print ""
            pointer -=  bytesPerPattern(stitches, rows)

        #for i in range (0x7eDF, 99*7, -1):
        #    print "\t",hex(i),": ",hex(bf.getIndexedByte(i))
        
        

else:
    print 'Searching for pattern number %d' % patt
    pats = bf.getPatterns(patt)
    if len(pats) == 0:
        print 'pattern %d not found' % patt
    else:
        stitches = pats[0]["stitches"]
        rows = pats[0]["rows"]
        print '%3d Stitches, %3d Rows' % (stitches, rows)
        pattern = bf.getPattern(patt)
        for row in range(rows):
            for stitch in range(stitches):
                if(pattern[row][stitch]) == 0:
                    print ' ',
                else:
                    print '*',
            print

