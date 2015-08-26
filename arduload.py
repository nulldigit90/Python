#! /usr/bin/python

# arduload.py
# By: Techb
# Date: Aug 26, 2015
# A script to compile and load arduino sketchs.
# This will check and make sure the tty is avail.
# In your sketch you need to have two comments at the
# the top of your file, example:
#     // --board arduino:avr:uno
#     // --port /dev/ttyUSB0
# --board, you will need the board your using.
# --port, is where your serail com is.
# Linux only, I don't plan to add Windows support
# since I don't use or have Windows. Feel free to add support.
# Tested on Arch Linux 4.1.5, Python 3.4.3

# Find more here: https://github.com/arduino/Arduino/blob/master/build/shared/manpage.adoc

import sys
import os

def usage():
    print("[??] Example: python arduload.py <file>")

def test_dev(p):
    tty = p.split("/")[-1]
    ld = os.listdir("/dev")
    if tty in ld:
        print("[+] Found %s, continuing." % p)
    else:
        print("[-] Port %s not found, try another..." % p)
        sys.exit("[!] Exiting...")

if len(sys.argv) < 2:
    usage()
    sys.exit()
else:
    sketch = sys.argv[1]

try:
    with open(sketch, "r") as fd:
        fl = [l for l in fd.readlines()]
        if "--board" in fl[0] and "--port" in fl[1]:
            board = fl[0].strip().split("--board")[-1].strip()
            print("[+] Using board %s" % board)
            # test the port
            port = fl[1].strip().split("--port")[-1].strip()
            test_dev(port)
            os.system("arduino --board %s --port %s --upload %s" % (board, port, sketch))
            print("[+] Done.")

except FileNotFoundError:
    print("[!] File not found. Try again.")
    usage()
    print("[!] Exiting...")
