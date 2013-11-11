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

version = '1.0'

if len(sys.argv) < 2:
    print 'Usage: %s file [start] [end]' % sys.argv[0]
    print 'Dumps both rows of needle data from brother data files'
    print 'Optional start and end needle numbers, default to 1 and 200'
    sys.exit()

leftend = 0
rightend = 200
if len(sys.argv) == 3:
    leftend = int(sys.argv[2])
if len(sys.argv) == 4:
    leftend = int(sys.argv[2])
    rightend = int(sys.argv[3])


bf = brother.brotherFile(sys.argv[1])

currentrow = bf.currentRow()
nextrow = bf.nextRow()

print '   Next:',
for stitch in nextrow[leftend:rightend]:
    if(stitch) == 0:
        print ' ',
    else:
        print '*',
print
print 'Current:',
for stitch in currentrow[leftend:rightend]:
    if(stitch) == 0:
        print ' ',
    else:
        print '*',
print

