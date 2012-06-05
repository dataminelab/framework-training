#!/usr/bin/env python

import sys, string, re

for line in sys.stdin:
    line = line.strip().lower()
    line = re.sub('[^A-Za-z0-9 ]+', '', line)
    words = line.split()
    for word in words:
        print '%s\t%s' % (word, 1)
