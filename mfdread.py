#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  mfdread.py - Mifare dumps parser in human readable format
#  Pavel Zhovner <pavel@zhovner.com>
#  https://github.com/zhovner/mfdread



import codecs
import sys
from struct import unpack 
from datetime import datetime



if len(sys.argv) == 1:
    print('''
------------------
Usage: mfdread.py ./dump.mfd
Mifare dumps reader. 
''')
    sys.exit();




class bashcolors:
    BLUE = '\033[34m'
    RED = '\033[91m'
    GREEN = '\033[32m'
    WARNING = '\033[93m'
    ENDC = '\033[0m'


def print_info(data):

    blocksmatrix = []

    # determine what dump we get 1k or 4k
    if len(data) == 4096:
        cardsize = 64
    elif len(data) == 1024:
        cardsize = 16
    else: 
        print("Wrong file size: %d bytes.\nOnly 1024 or 4096 allowed." % len(data))
        sys.exit();

    # read all sectors
    for i in range(0, cardsize):
        start = i * 64
        end   = (i + 1) * 64
        sector = data[start:end]
        sector = codecs.encode(sector, 'hex')
        if not type(sector) is str:
            sector = str(sector, 'ascii')
        blocksmatrix.append([sector[x:x+32] for x in range(0, len(sector), 32)])

    # add colors for each keyA, access bits, KeyB
    for c in range(0, len(blocksmatrix)):
        keyA =  bashcolors.RED + blocksmatrix[c][3][0:12] + bashcolors.ENDC
        accbits = bashcolors.GREEN + blocksmatrix[c][3][12:20] + bashcolors.ENDC
        keyB =  bashcolors.BLUE + blocksmatrix[c][3][20:32] + bashcolors.ENDC
        blocksmatrix[c][3] = keyA + accbits + keyB

    print("File size: %d bytes. Expected %d sectors" %(len(data),cardsize))
    print("\n\tUID:  " + blocksmatrix[0][0][0:8])
    print("\tBCC:  " + blocksmatrix[0][0][8:10])
    print("\tSAK:  " + blocksmatrix[0][0][10:12])
    print("\tATQA: " + blocksmatrix[0][0][12:14])
    print("                   %sKey A%s    %sAccess Bits%s    %sKey B%s" %(bashcolors.RED,bashcolors.ENDC,bashcolors.GREEN,bashcolors.ENDC,bashcolors.BLUE,bashcolors.ENDC))
    print("╔═════════╦═════╦══════════════════════════════════╗")
    print("║  Sector ║Block║            Data                  ║")
    for q in range(0, len(blocksmatrix)):
        print("╠═════════╬═════╬══════════════════════════════════╣")
        for z in range(0, len(blocksmatrix[q])):
            if (z == 2):
                if (len(str(q)) == 1):
                    print("║    %d    ║  %d  ║ %s ║"  %(q,z,blocksmatrix[q][z]))
                if (len(str(q)) == 2):
                    print("║    %d   ║  %d  ║ %s ║"  %(q,z,blocksmatrix[q][z]))
                if (len(str(q)) == 3):
                    print("║    %d ║  %d  ║ %s ║"  %(q,z,blocksmatrix[q][z]))
            else:
                print("║         ║  %d  ║ %s ║"  %(z,blocksmatrix[q][z]))
    print("╚═════════╩═════╩══════════════════════════════════╝")


def main(filename):
    with open(filename, "rb") as f:
        data = f.read()
        print_info(data)
 
if __name__ == "__main__":
    main(sys.argv[1])
