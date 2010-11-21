#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from urllib import urlencode
import urllib2
import re
import HTMLParser

import pdb

class Google():
    def __init__(self):
        self.html_parser = HTMLParser.HTMLParser()
            
    def getKeywords(self, keyword, *args, **kwargs):
        
        def __get_g_json(term): 
            data = urllib2.urlopen('http://clients1.google.it/complete/search?'+urlencode({'q':term.encode('utf-8'), 'hl':'it', 'client':'hp'})).read()
            HTMLtag = re.compile('<\/*b>')      # Matches HTML tags
            data = unicode(data, 'iso-8859-15')
            g_list = json.loads(data[19:-1])
            return [self.html_parser.unescape(HTMLtag.sub('', entry[0])) for entry in g_list[1]]
        
        keywords = list()
        g_json=__get_g_json(unicode(keyword, 'utf-8'))
        for entry in g_json[1:]:
            keywords.append(entry)
        add_keywords = list()
        for keyword in keywords[1:]:
            g_json = __get_g_json(keyword)
            for entry in g_json[1:3]:
                add_keywords.append(entry)
        keywords.extend(add_keywords)
        return keywords
