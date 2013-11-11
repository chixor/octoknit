#/usr/bin/bash

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

convert -size 280x40 xc:white -colors 2 +antialias -font courier -pointsize 40 -draw "text 10,32 'Hello World'" -rotate -90 testa.png

#convert -size 280x40 xc:white -colors 2 +antialias -font courier -pointsize 40 -draw "text 10,32 'Hello World'" testa.png

#convert -size 460x72 xc:white -colors 2 +antialias -font Bookman-DemiItalic -pointsize 72 -draw "text 10,60 'Hello World'" testa.png

