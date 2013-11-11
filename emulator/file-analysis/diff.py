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

import sys
import brother

if len(sys.argv) < 3:
    print 'Usage: %s fileA fileB' % sys.argv[0]
    sys.exit()

b1 = brother.brotherFile(sys.argv[1])
b2 = brother.brotherFile(sys.argv[2])

# Selector Mode
# Pattern Start
# Motif information
# Custom pattern list, patterns, memo info
# Memo data
# Pattern Number
# Current Row Number
# Unknowns from 0x0700 to 0x0715
# Unknowns from 0x07D0 to 0x07E9

sel1 = b1.selectorValue()
sel2 = b2.selectorValue()

print 'Selector    %4d     %4d' % (sel1, sel2)

pn1 = b1.patternNumber()
pn2 = b2.patternNumber()
print 'Pattern #   %4d     %4d' % (pn1, pn2)

memo1 = b1.getMemo()
memo2 = b2.getMemo()
print 'memo len    %4d     %4d' % (len(memo1), len(memo2))

rn1 = b1.rowNumber()
rn2 = b2.rowNumber()
print 'row number  %4d     %4d' % (rn1, rn2)

cs1 = b1.carriageStatus()
cs2 = b2.carriageStatus()
print 'carr status 0x%02X     0x%02X' % (cs1, cs2)

md1 = b1.motifData()
md2 = b2.motifData()
for i in range(len(md1)):
    one = md1[i]
    two = md2[i]
    print 'mot %2d pos %4d %s  %4d %s' % (i+1, one['position'], one['side'], two['position'], two['side']),
    print 'mot %2d cnt %4d     %4d' % (i+1, one['copies'], two['copies'])    
print

pp1 = b1.patternPosition()
pp2 = b2.patternPosition()
print 'pattern pos %4d %s %4d %s' % (pp1['position'], pp1['side'], pp2['position'], pp2['side'])

print

uk1 = b1.unknownOne()
uk2 = b2.unknownOne()
print 'Unknown One:'
for i in range(len(uk1)):
    if uk1[i] or uk2[i]:
        print '     %4d     %4d' % (uk1[i], uk2[i]),
        if (uk1[i] != uk2[i]):
            print '  <======'
        else:
            print
    
print 'Unknown Memo Range:'
uk1 = b1.unknownMemoRange()
uk2 = b2.unknownMemoRange()
for i in range(len(uk1)):
    if uk1[i] or uk2[i]:
        print '     %4d     %4d' % (uk1[i], uk2[i]),
        if (uk1[i] != uk2[i]):
            print '  <======'
        else:
            print
    
print 'Unknown End Range:'
uk1 = b1.unknownEndRange()
uk2 = b2.unknownEndRange()
for i in range(len(uk1)):
    if uk1[i] or uk2[i]:
        print '     %4d     %4d' % (uk1[i], uk2[i]),
        if (uk1[i] != uk2[i]):
            print '  <======'
        else:
            print
    
print 'Individual unknowns:'
b1lst = b1.unknownAddrs()
b2lst = b2.unknownAddrs()
for i in range(len(b1lst)):
    lt = b1lst[i]
    lval = b1.getIndexedByte(lt[1])
    rval = b2.getIndexedByte(lt[1])
    print '0x%s   0x%02X   0x%02X  (%3d)  (%3d)' % (lt[0], lval, rval, lval, rval),
    if lval != rval:
        print '<----'
    else:
        print

