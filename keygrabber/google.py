#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 10/02/2011
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''
import unittest
import json
from html.parser import HTMLParser
from urllib.parse import urlencode
import urllib.request, urllib.error, urllib.parse
import re
import time

max_answers = 10

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
		self.html_parser = HTMLParser()
		self.open_function = urllib.request.urlopen
		if proxy:
			proxy_handler = urllib.request.ProxyHandler(proxy)
			self.opener = urllib.request.build_opener(proxy_handler)
			self.open_function = self.opener.open
            
	def getInstantKeys(self, keyword, *args, **kwargs):
		
		def __get_g_json(term):
			while True:
				try: 
					data = self.open_function('http://clients1.google.it/complete/search?'+urlencode({'q':term.encode('utf-8'), 'hl':'it', 'client':'hp'})).read()
					break
				except urllib.error.HTTPError as e:
					if e.code == 400:
						#we reached the end of the expansion
						return []
					time.sleep(10)
					continue
			HTMLtag = re.compile('<\/*b>')      # Matches HTML tags
			data = data.decode('iso-8859-15')
			if data[0:18] != 'window.google.ac.h':
				raise NotValidAnswerError('answer is not valid')
			try:
				g_list = json.loads(data[19:-1])
			except:
				return []
				
			return [self.html_parser.unescape(HTMLtag.sub('', entry[0])) for entry in g_list[1]]
		
		keywords = list()
		g_json=__get_g_json(keyword)
		if keyword in g_json:
			g_json.remove(keyword)
		for entry in g_json:
			keywords.append(entry)
		return keywords

	def search(self, keyword, *args, **kwargs):
		return self.getInstantKeys(keyword)
		
	def expand(self, keyword, level=0):
		'''
		Returns an iterator which returns (expanded key, level) for each subkey found
		'''
		for item in self.getInstantKeys(keyword+' '):
			yield (item, level)
			for subitem in self.expand(item, level + 1):
				yield subitem
    
class GoogleTest(unittest.TestCase):
	
    def test_a_single_request(self):
        google = Google()
        search = ['test', 'testa', 'com', 'come']
        for word in search:
            res = google.search(word)
            self.assertEqual(word in res, False)
    
    def test_400_error(self):
        google = Google()
        res = google.expand('come due numeri primi separati da un solo numero pari. vicini ma mai abbastanza per toccarsi')
        self.assertEqual(len(res), 1)
    
    @unittest.skip("Should be updated to python 3")
    def test_tor(self):
       
        def get_ip(page):
            return page[page.find('<span class="ip blue">')+22:page.find('<!-- contact us before using')]
        
        import settings
        google=Google(settings.proxy)
        tor_page = google.open_function('http://whatismyipaddress.com/').read()
        page = urllib.request.urlopen('http://whatismyipaddress.com/').read()
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
        r_search = ['come', 'come arredare casa']
        for key in r_search:
            for item in google.expand(key):
                print(item)
            
           
    def test_max_answer(self):
        google = Google()
        r_search = ['come ']
        for key in r_search:
            self.assertEqual(len(google.search(key)), max_answers)
            
            
if __name__ == '__main__':
    unittest.main()
        
