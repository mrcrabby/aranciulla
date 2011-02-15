#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 10/02/2011
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''
import unittest
import json
import HTMLParser
from urllib import urlencode
import urllib2
import re
import time


class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class NotValidAnswerError(Error):
    """Exception raised for errors in the input.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg


class Google():
    def __init__(self, proxy=None):
        self.html_parser = HTMLParser.HTMLParser()
        self.open_function = urllib2.urlopen
        if not proxy:
            proxy_handler = urllib2.ProxyHandler(proxy)
            self.opener = urllib2.build_opener(proxy_handler)
            self.open_function = self.opener.open
            
    def getInstantKeys(self, keyword, *args, **kwargs):
        
        def __get_g_json(term):
            while True:
                try: 
                    data = self.open_function('http://clients1.google.it/complete/search?'+urlencode({'q':term.encode('utf-8'), 'hl':'it', 'client':'hp'})).read()
                    break
                except:
                    time.sleep(10)
                    continue
            HTMLtag = re.compile('<\/*b>')      # Matches HTML tags
            data = unicode(data.decode('iso-8859-15'))
            if data[0:18] != 'window.google.ac.h':
                raise NotValidAnswerError('answer is not valid')
            g_list = json.loads(data[19:-1])
            return [self.html_parser.unescape(HTMLtag.sub('', entry[0])) for entry in g_list[1]]
        
        keywords = list()
        g_json=__get_g_json(unicode(keyword))
        if keyword in g_json:
            g_json.remove(keyword)
        for entry in g_json:
            keywords.append(entry)
        return keywords

    def search(self, keyword, *args, **kwargs):
        return self.getInstantKeys(keyword)
    
class GoogleTest(unittest.TestCase):
    def test_search(self):
        google = Google()
        keys = ['jzs','comeee']
        for key in keys:
            search = google.search(key)
            self.assertEqual(search, [])
            
if __name__ == '__main__':
    unittest.main()
        