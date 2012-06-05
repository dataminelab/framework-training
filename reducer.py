#!/usr/bin/env python

from operator import itemgetter
import sys

last_word = None
current_count = 0
word = None

for line in sys.stdin:
    line = line.strip()

    word, count = line.split('\t', 1)

    if last_word == word:
        current_count += int(count)
    else:
        if last_word:
            print '%s\t%s' % (last_word, current_count)
        current_count = int(count)
        last_word = word

if last_word == word:
    print '%s\t%s' % (last_word, current_count)
    
