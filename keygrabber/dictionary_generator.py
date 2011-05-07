#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 10/02/2011
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''

import sys
import unittest
import itertools
import string

class SmartDict(object):
    def __init__(self, **kwargs):
        self.seq = kwargs.get('seq', string.ascii_lowercase)
        self.size = kwargs.get('size', 3)
        self.blacklist = kwargs.get('blacklist', [])
        self.actual = None
    
    def __iter__(self):
        return self

    def get(self, **kwargs):
        seq = kwargs.get('seq', self.seq)
        size = kwargs.get('size', self.size)
        blacklist = kwargs.get('blacklist', self.blacklist)
        self.actual = ''
        yield ''
        for p in itertools.chain.from_iterable(map(lambda x: itertools.product(seq, repeat=x), range(1,size+1))):
            joined = ''.join(p)
            if not any(joined.startswith(prefix) for prefix in blacklist):
                self.actual = joined
                yield joined

    def jump(self):
        self.blacklist.append(self.actual)
        
class SmartDictTest(unittest.TestCase):
    
	def test_newdictionary(self):
		c = SmartDict(seq=string.ascii_lowercase, size=3)
		banned = ['c', 'd', 'zz']
		result = []
		for p in c.get():
			if p in banned:
				c.jump()
				result.append(p)
        #maybe fake, do not trust:
		self.assertTrue(any(x.startswith(y) for x in result for y in banned), False)
       
if __name__ == '__main__':
    sys.exit(unittest.main())
