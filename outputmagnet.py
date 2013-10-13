#!/usr/bin/python
# -*- coding: utf-8 -*-

with open('magnet.txt', 'wb') as f:
    for line in open('output.txt'):
        words = line.split('\t')
        print >>f, words[2]
        
