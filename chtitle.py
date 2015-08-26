#! /usr/bin/python2

import sys

if len(sys.argv) < 2:
    print "Usage: chtitle <title name>"
    sys.exit()

print("\x1b]2;%s\x07" % sys.argv[1])
#sys.stdout.write("\x1b]2;%s\x07" % sys.argv[1])
