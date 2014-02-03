#!/usr/bin/python
# -*- coding: utf-8 -*-


import re
import sys
import urllib
import codecs
from pyquery import PyQuery as pq
from subprocess import Popen, PIPE
import multiprocessing

username = 'clowwindy'
pages = 8


class attrdict(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)
        self.__dict__ = self

def get_page(url):
    curl = Popen(('curl', '-H', 'Accept-Language: en-US', '-L', url) , shell=False, bufsize=0, stdin=PIPE, 
    stdout=PIPE, stderr=PIPE, close_fds=True )
    
    content = curl.stdout.read()
    if curl.wait() == 0:
        return content
    return None
    
def get_douban_list_page(page):
    url = 'http://movie.douban.com/people/%s/wish?start=%d&sort=time&rating=all&filter=all&mode=list' % (username, page * 30)
    return get_page(url)
   
    
def parse_douban_list_page(content):
    doc = pq(content)
    rows = doc.find('#content .list-view .item-show')
    items = []
    for row in rows:
        row = pq(row)
        title_a = row.find('a')
        if not title_a:
            continue
        link = title_a.attr('href')
        items.append(link)
    return items

def parse_douban_item_page(content):
    doc = pq(content)
    a = doc.find('#info a[href^=http\\:\\/\\/www\\.imdb\\.com\\/title]')
    if a:
        link = a.attr('href')
        return link
    else:
        return None

def parse_imdb(content):
    doc = pq(content)
    return doc.find('h1.header .itemprop').text() + ' ' + doc.find('h1.header .nobr').text()

all_links = []

for i in range(0, pages):
    content = get_douban_list_page(i)
    links = parse_douban_list_page(content)
    all_links.extend(links)

def process(link):
    item_page = get_page(link)
    imdb_link = parse_douban_item_page(item_page)
    if imdb_link:
        imdb_page = get_page(imdb_link)
        try:
            print parse_imdb(imdb_page)
        except:
            pass

p = multiprocessing.Pool(5)
p.map(process, all_links)

