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

#
# Pattern Number
# Position of the selector
# Pattern position for the selector setting
# Pattern position and number of repeats for each motif for selector (2) settings
# Variation key settings
# Memo display information
# Row numbers and memo key information

# 200 needles
# pattern position is Yellow or Green (left or right)
# up to 6 motifs - 

import sys
from struct import *
from collections import namedtuple
#import os
#import os.path
#import string
#from array import *

def dumpPattern(pat):
    bits = []
    for short in pat:
        for i in range(15, -1, -1):
            mask = (2 ** i)
            if short & (2 ** i):
                bits.append('*')
            else:
                bits.append(' ')
    print "".join(bits)
    return


if len(sys.argv) < 3:
    print 'Usage: %s fileA fileB' % sys.argv[0]
    sys.exit()

f1 = open(sys.argv[1])
#f2 = open(sys.argv[2])

d1 = f1.read(2048)
#d2 = f2.read(2048)

# head - 1766 bytes
fmt = '1766B'
# first pattern
fmt += '13H'
# after first pattern
fmt += '22B'


# second pattern
fmt += '13H'
# tail
fmt += '208B'


#lead, pattern1, dummy, pattern2, tail = struct.unpack(fmt, d1)
#lead[1766], pattern1[13], dummy[22], pattern2[13], tail[208] = unpack(fmt, d1)
foo = unpack(fmt, d1)
print len(foo)
#bar = foo[0:1766]
baz = foo[1766:1779]
dumpPattern(baz)
#print bar
#print baz
#print foo

#inrun = False
#for i in range(len(d1)):
#    if d1[i] != d2[i]:
#        if not inrun:
#            print '--'
#            inrun = True
#        print '%04X: %02X %02X' % (i, ord(d1[i]), ord(d2[i]))
#    else:
#        inrun = False
#
#f1.close()
#f2.close()
