#!/usr/bin/env python

# Copyright 2012  Steve Conklin 
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
import os
#import os.path
#import string
import time
import serial

from FDif import PDD1, dump

# meat and potatos here

if len(sys.argv) < 3:
    print 'Usage: %s serialdevice dirname' % sys.argv[0]
    print
    print 'Reads all sectors and sector IDs from a disk and'
    print 'copies it into the directory specified.'
    print 'The format is the same as PDDemulate uses.'
    sys.exit()


bdir = os.path.relpath(sys.argv[2])
print "bdir = ", bdir
if os.path.exists(bdir):
    print "<%s> already exists, exiting . . ." % bdir
    sys.exit()

os.mkdir(bdir)

drive = PDD1()

drive.open(cport=sys.argv[1])

for sn in range(80):
    ifn = "%02d.id" % sn
    dfn = "%02d.dat" % sn
    Fid = open(os.path.join(bdir, ifn), 'w')
    Fdata = open(os.path.join(bdir, dfn), 'w')

    sid = drive.FDCreadIdSection(psn = '%d' % sn)
    print "Sector %02d ID: " % sn
    print dump(sid)
    Fid.write(sid)

    data = drive.FDCreadSector(psn = '%d' % sn)
    print "Sector %02d Data: " % sn
    print dump(data)
    Fdata.write(data)

    Fid.close()
    Fdata.close()

    if sn % 2:
        filenum =  ((sn-1)/2)+1
        filename =  'file-%02d.dat' % filenum
        # we wrote an odd sector, so create the
        # associated file
        fn1 = os.path.join(bdir, '%02d.dat' % (sn-1))
        fn2 = os.path.join(bdir, '%02d.dat' % sn)
        outfn =  os.path.join(bdir, filename)
        cmd = 'cat %s %s > %s' % (fn1, fn2, outfn)
        os.system(cmd)

drive.close()
