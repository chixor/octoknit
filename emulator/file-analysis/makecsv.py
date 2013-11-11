#!/usr/bin/env python

# Copyright 2010  Steve Conklin 
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

# Take existing files in a base directory and convert them
# to a csv file for importing in a spreadsheet

import sys
#import os
#import os.path
#import string
#from array import *

if len(sys.argv) < 2:
    print 'Usage: %s basedir' % sys.argv[0]
    sys.exit()

f = []
d = []

for idx in range(10):
    fname = sys.argv[1] + "/file-%02d.dat" % (idx + 1)
    #print "trying %s" % fname
    try:
        fd = open(fname)
        f.append(fd)
        d.append(fd.read(2048))
        fd.close()
    except IOError:
        break

# Now dump to a csv

# Header row
print 'Address, Notes',
for fnum in range(len(f)):
    print ', file-%02d' % (fnum+1),
print ""

# Spare rows
print ','
print ','
print ','



# data rows
for i in range(2048):
    print '0x%04X,' % i,
    # Add comment fields here
    for fnum in range(len(f)):
        print ', 0x%02X' % ord(d[fnum][i]),
    print ""
