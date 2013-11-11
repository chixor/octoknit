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
#import os
#import os.path
#import string
import time
import serial

FILTER=''.join([(len(repr(chr(x)))==3) and chr(x) or '.' for x in range(256)])

def dump(src, length=16):
    result=[]
    for i in xrange(0, len(src), length):
       s = src[i:i+length]
       hexa = ' '.join(["%02X"%ord(x) for x in s])
       printable = s.translate(FILTER)
       result.append("%04X   %-*s   %s\n" % (i, length*3, hexa, printable))
    return ''.join(result)

class PDD1():

    def __init__(self):
        self.verbose = False
        self.commport = ''
        self.ser = None
        return

    def __del__(self):
        return

    def open(self, cport='/dev/ttyUSB0', rate = 9600, par = 'N', stpbts=1, tmout=None, xx=0):
        self.ser = serial.Serial(port = cport, baudrate = rate, parity = par, stopbits = stpbts, timeout = tmout, xonxoff=0, rtscts=1, dsrdtr=0)
        if self.ser == None:
            print 'Unable to open serial device %s' % cport
            raise IOError
        self.commtimeout = tmout
        # Sometimes on powerup there are some characters in the buffer, purge them
        self.dumpchars()
        return

    def close(self):
        if self.ser is not None:
            self.ser.close()
            self.ser = None
        return

    def dumpchars(self):
        num = 1
        while self.ser.inWaiting():
            inc = self.ser.read()
            if len(inc) != 0:
                print 'flushed 0x%02X (%d)' % (ord(inc), num)
                num = num + 1
            else:
                break
        return

    def getFDCresponse(self, expected):
        sch = self.ser.read(expected)
        return sch

    def isSuccess(self, FDCstatus):
        if self.verbose:
            print "isSuccess checking:"
            print dump(FDCstatus)
            if (FDCstatus[0] == '0') and (FDCstatus[1] == '0'):
                print "  SUCCESS"
                print "  Physical Sector = %c%c" % (FDCstatus[2], FDCstatus[3])
                print "  Logical Sector  = %c%c%c%c" %  (FDCstatus[4], FDCstatus[5],FDCstatus[6], FDCstatus[7])
            else:
                print "  ***** ERROR ***** : %c%c" %  (FDCstatus[0], FDCstatus[1])
                print "  Physical Sector = %c%c" % (FDCstatus[2], FDCstatus[3])
                print "  Logical Sector  = %c%c%c%c" %  (FDCstatus[4], FDCstatus[5],FDCstatus[6], FDCstatus[7])
        if len(FDCstatus) != 8:
            print "Status Bad Len"
            return False
        for sb in FDCstatus[0:2]:
            if sb != '0':
                return False
        return True

#    def readchar(self):
#        inc = ''
#        while len(inc) == 0:
#            inc = self.ser.read()
#        return inc
            
    def writebytes(self, bytes):
        self.ser.write(bytes)
        return

    def calcChecksum(self, string):
        sum = 0
        for schr in string:
            sum = sum + ord(schr)
        sum = sum % 0x100
        sum = sum ^ 0xFF
        return chr(sum)

#    def __commandResponse(self, command):
#        if self.verbose:
#            pcmd = command.strip()
#            print 'writing command ===> <%s>' % pcmd
#        self.dumpchars()
#        ds_string = command
#        cs = self.calcChecksum(ds_string)
#        ds_string = ds_string + cs
#        print "cR sending . . ."
#        print dump(ds_string)
#        self.writebytes(ds_string)
#        response = self.readsomechars()
#        print 'Command got a response of ', response
#        return response

    def __FDCcommandResponse(self, command, expected):
        if self.verbose:
            pcmd = command.strip()
            print '-------------------------------------\nwriting FDC command ===> <%s>' % pcmd
        self.dumpchars()
        self.writebytes(command)
        response = self.getFDCresponse(expected)
        return response
    #
    # Begin Op Mode commands
    #

    def EnterFDCMode(self):
        if False:
            command = "ZZ" + chr(0x08) + chr(0)
            cs = self.calcChecksum(command)
            command = command + cs + "\r"
        else:
            command = "ZZ" + chr(0x08) + chr(0) + chr(0xF7) + "\r"
        if self.verbose:
            print "Entering FDC Mode, sending:"
            print dump(command),
        self.writebytes(command)
        # There's no response to this command, so allow time to complete
        time.sleep(.010)
        if self.verbose:
            print "Done entering FDC Mode\n"
        return

    #
    # Begin FDC mode commands
    #

    def FDCChangeMode(self, mode = '1'):
        """
        Change the disk drive mode. Default to changing from FDC
        emulation mode back to Operational Mode.
        """
        command = "M " + mode
        result = self.__FDCcommandResponse(command, 8)
        if not self.isSuccess(result):
            raise IOError
        return

    def FDCcheckDeviceCondition(self):
        """
        Send the 'D' command and return the result
        """
        command = "D\r"
        result = self.__FDCcommandResponse(command, 8)
        if self.verbose:
            # third byte:
            # 30 - Normal
            # 45 - Door open or no disk
            # 32 - write protected
            print "third byte = 0x%X" % ord(result[2])
        return result

    def FDCformat(self, sectorSize='5', verify=True):
        """
        Format the floppy with the requested 
        """
        if verify:
            command = "F"
        else:
            command = "G"
        command = command + sectorSize + "\r"
        result = self.__FDCcommandResponse(command, 8)
        if not self.isSuccess(result):
            raise IOError
        return

    def FDCreadIdSection(self, psn = '0'):
        """
        Read the ID section of a physical sector, and return
        the ID, which should be 12 bytes long
        """
        if self.verbose:
            print "FDCreadIdSection: Enter"
        command = "A " + psn + "\r"
        result = self.__FDCcommandResponse(command, 8)
        if not self.isSuccess(result):
            raise IOError
        result =  self.__FDCcommandResponse("\r", 12)
        if self.verbose:
            print "FDCreadIdSection data:"
            print dump(result)
            print "FDCreadIdSection: Exit"
        return result

    def FDCreadSector(self, psn = '0', lsn = '1'):
        """
        Read the data from a logical sector.
        psn is Physical sector number, in the range 0-79
        lsn is the logical sector  number, in range of 1
        to the max for the physical sector size
        """
        if self.verbose:
            print "FDCreadSector: Enter"
        command = "R " + psn + ","+ lsn + "\r"
        result = self.__FDCcommandResponse(command, 8)
        if not self.isSuccess(result):
            raise IOError
        if self.verbose:
            print "FDCreadSector: Phase two"
        result =  self.__FDCcommandResponse("\r", 1024)
        if self.verbose:
            print "FDCreadSector data:"
            print dump(result)
            print "FDCreadSector: Exit"
        return result

    def FDCsearchIdSection(self, data, psn = '0'):
        """
        Compare the data to the sector ID
        psn is Physical sector number, in the range 0-79
        Data length must be 12 bytes
        """
        if len(data) != 12:
            raise ValueError("ID data must be 12 characters long")
        if self.verbose:
            print "FDCsearchIdSection: Enter"
        command = "S" + psn + "\r"
        result = self.__FDCcommandResponse(command, 8)
        if not self.isSuccess(result):
            raise IOError
        if self.verbose:
            print "FDCsearchIdSection data:"
            print dump(data)
        result =  self.__FDCcommandResponse(data, 12)
        if self.verbose:
            print "FDCsearchIdSection: Exit"
        print "NOT SURE WHAT WE EXPECT HERE"
        print "FDCsearchIdSection status is:"
        print dump(result)
        if not self.isSuccess(result):
            raise IOError
        return

    def FDCwriteIdSection(self, data, psn = '0', verify = True):
        """
        Write the data to the sector ID
        psn is Physical sector number, in the range 0-79
        Data length must be 12 bytes
        """
        if len(data) != 12:
            raise ValueError("ID data must be 12 characters long")
        if verify:
            command = "B"
        else:
            command = "C"
        if self.verbose:
            print "FDCwriteIdSection: Enter"
        command = command + psn + "\r"
        result = self.__FDCcommandResponse(command, 8)
        if not self.isSuccess(result):
            raise IOError
        if self.verbose:
            print "FDCwriteIdSection data:"
            print dump(data)
        result =  self.__FDCcommandResponse(data, 8)
        if self.verbose:
            print "FDCwriteIdSection: Exit"
        if not self.isSuccess(result):
            raise IOError
        return

#W     Write log sector w/verify   
#      (two stages - second stage send data to be written)
#X     Write log sector w/o vfy    
#      (two stages - second stage send data to be written)
    def FDCwriteSector(self, data, psn = '0', lsn = '1', verify = True):
        """
        Write the data to the sector
        psn is Physical sector number, in the range 0-79, defaults to 0
        lsn is logical sector number, defaults to 1
        """
        if verify:
            command = "W"
        else:
            command = "X"
        if self.verbose:
            print "FDCwriteSector: Enter"
        command = command + psn + "," + lsn + "\r"
        result = self.__FDCcommandResponse(command, 8)
        if not self.isSuccess(result):
            raise IOError
        if self.verbose:
            print "FDCwriteSector data:"
            print dump(data)
        result =  self.__FDCcommandResponse(data, 8)
        if self.verbose:
            print "FDCwriteSector: Exit"
        if not self.isSuccess(result):
            raise IOError
        return
