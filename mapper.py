#!/usr/bin/env python

import sys, string

for line in sys.stdin:
    line = line.strip().translate(None, string.punctuation).lower()
    words = line.split()
    for word in words:
        print '%s\t%s' % (word, 1)
