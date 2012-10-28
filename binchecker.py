#binchecker.py
#Binchecker is a simple utility script written in Python for injecting CRC
#checksums in small binary files.
#
#This software is licensed under the terms of the OSI-MIT license.
#Copyright (c) 2012 @adamsch
#
#Permission is hereby granted, free of charge, to any person obtaining a copy of 
#this software and associated documentation files (the "Software"), to deal in 
#the Software without restriction, including without limitation the rights to 
#use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
#the Software, and to permit persons to whom the Software is furnished to do so, 
#subject to the following conditions:
#
#The above copyright notice and this permission notice shall be included in all 
#copies or substantial portions of the Software.
#
#THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
#IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
#FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE 
#AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
#LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, 
#OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE 
#SOFTWARE.

#!/usr/bin/python

"""
CRC algorithm:
http://crcmod.sourceforge.net/crcmod.html
http://pypi.python.org/pypi/crcmod/1.7

"""

import sys, os
import struct
import crcmod


# Define the start address and the location of the CRC checksum
FLASH_START_ADDRESS   = 0x2000000
CRC_CHECKSUM_LOCATION = 0x3FFFFFF

# Open the file
try:
    path = sys.argv[1]
    f = open(path, 'r+b')
except:
    # Eventually this should give more useful information (e.g. file does not
    # exist, or not an image file, or ...
    print "Unable to open %s" % sys.argv[1]
    exit(-1)

# Get the file size
statinfo = os.stat(path)
fsize = statinfo.st_size
print fsize
if (fsize % 4 != 0):
  print "Must be an error, binary is not word aligned"
  exit(-1)

# Make a string from the bytes
binChars = []
for i in range(0,fsize-4):
  f.seek(i)
  nextChar = f.read(1)
  binChars.append(nextChar)
  #print nextChar
fstring = ''.join(binChars)

# Calculate CRC CCITT-32
crc32_func = crcmod.mkCrcFun(0x104c11db7, initCrc=0, xorOut=0xFFFFFFFF)
crcm = crc32_func(fstring) & 0xffffffff
print hex(crcm)
fcrcbin = struct.pack('L', crcm)

#Read the entire file and load it into a list
f.seek(0)
fdata = list(f.read())
# Close the file
f.close()

# Open the file for writing
try:
    f = open(path, 'wb')
except:
    # Eventually this should give more useful information (e.g. file does not
    # exist, or not an image file, or ...
    print "Unable to open %s" % sys.argv[1]
    exit(-1)

print "test:"
print len(fdata)
print hex(crc32_func('12345678')) #0x9ae0daaf
fdata[fsize-4:fsize] = fcrcbin
fdatastr = ''.join(fdata)
f.write(fdatastr)

# Close the file
f.close()
