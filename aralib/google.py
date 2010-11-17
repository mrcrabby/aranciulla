#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from urllib import urlencode
import urllib2
import re

def get_google_keywords(keyword, *args, **kwargs):
    
    def __get_g_json(term):
        data = urllib2.urlopen('http://clients1.google.it/complete/search?'+urlencode({'q':term, 'hl':'it', 'client':'hp'})).read()
        HTMLtag = re.compile('<\/*b>')      # Matches HTML tags
        g_list = json.loads(data[19:-1])
        return [HTMLtag.sub('', entry[0]) for entry in g_list[1]]
    
    keywords = list()
    g_json=__get_g_json(keyword)
    for entry in g_json:
        keywords.append(entry)
    add_keywords = list()
    print keywords
    for keyword in keywords[1:]:
        print 
        g_json = __get_g_json(keyword)
        print g_json
        for entry in g_json[1:3]:
            add_keywords.append(entry)
    keywords.extend(add_keywords)
