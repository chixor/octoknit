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

#
# Compare two files and dump the differences
#

import sys
if len(sys.argv) < 3:
    print 'Usage: %s fileA fileB' % sys.argv[0]
    sys.exit()

f1 = open(sys.argv[1])
f2 = open(sys.argv[2])

d1 = f1.read(2048)
d2 = f2.read(2048)

inrun = False
for i in range(len(d1)):
    if d1[i] != d2[i]:
        if not inrun:
            print '--'
            inrun = True
        print '%04X: %02X %02X | %03d %03d' % (i, ord(d1[i]), ord(d2[i]), ord(d1[i]), ord(d2[i]))
    else:
        inrun = False

f1.close()
f2.close()
