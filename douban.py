#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import urllib
import codecs
from pyquery import PyQuery as pq
from subprocess import Popen, PIPE

username = 'clowwindy'
pages = 3

def get_douban_page(page, pages):
    url = 'http://movie.douban.com/people/%s/wish?start=%d&sort=time&rating=all&filter=all&mode=list' % (username, page)
    
    curl = Popen(('curl', '--socks5-hostname', '127.0.0.1:1080', url) , shell=False, bufsize=0, stdin=PIPE, 
    stdout=PIPE, stderr=PIPE, close_fds=True )
    
    content = curl.stdout.read()
    if curl.wait() == 0:
        return content
    return None

print get_douban_page(1, 3)