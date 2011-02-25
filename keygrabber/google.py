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
        if proxy:
            proxy_handler = urllib2.ProxyHandler(proxy)
            self.opener = urllib2.build_opener(proxy_handler)
            self.open_function = self.opener.open
            
    def getInstantKeys(self, keyword, *args, **kwargs):
        
        def __get_g_json(term):
            while True:
                try: 
                    data = self.open_function('http://clients1.google.it/complete/search?'+urlencode({'q':term.encode('utf-8'), 'hl':'it', 'client':'hp'})).read()
                    break
                except urllib2.HTTPError, e:
                    print e
                    print term
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
    
    def expand(self, keyword, *args, **kwargs):
        results = list()
        res = self.getInstantKeys(keyword+' ')
        for r in res:
            results.extend(self.expand(r))
        return res + results
    
class GoogleTest(unittest.TestCase):
    
    def test_tor(self):
       
        def get_ip(page):
            return page[page.find('<span class="ip blue">')+22:page.find('<!-- contact us before using')]
        
        import settings
        google=Google(settings.proxy)
        tor_page = google.open_function('http://whatismyipaddress.com/').read()
        page = urllib2.urlopen('http://whatismyipaddress.com/').read()
        tor_res = get_ip(tor_page)
        res = get_ip(page)
        self.assertNotEqual(tor_res, res)
        
    def test_search(self):
        google = Google()
        keys = ['jzs','comeee']
        for key in keys:
            search = google.search(key)
            self.assertEqual(search, [])
            
    def test_expand(self):
        google = Google()
        r_search = ['come']
        for key in r_search:
           google.expand(key)
           
            
            
if __name__ == '__main__':
    unittest.main()
        