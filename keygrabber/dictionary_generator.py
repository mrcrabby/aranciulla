#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Created on 10/02/2011
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''

import sys
import pdb

class Error(Exception):
    """Base class for exceptions in this module."""
    pass

class RangeError(Error):
    """Exception raised for errors in the input.

    Attributes:
        msg  -- explanation of the error
    """

    def __init__(self, msg):
        self.msg = msg


class Dictionary:
    '''
    Handles a dictionary which is depth characters long
    '''
    def __init__(self, startvalue, depth=3):
        self.depth = depth - 1
        self.value = [ord(startvalue)-1]
    
    def next(self):
        self.value[-1] = self.value[-1]+1
        for i,v in enumerate(self.value[::-1]):
            i = len(self.value) - i - 1
            if self.value[i] > 122:
                self.value[i] = 97
                if i==0:
                    self.value.insert(0,97)
                else:
                    self.value[i-1] = self.value[i-1]+1
                if len(self.value) > self.depth and self.value[0] > 122:
                    raise RangeError('Range limit reached')
                
                    
        return unicode(''.join([chr(x) for x in self.value]))
        

def test():
    di = Dictionary('a',3)
    for i in range(15000000):
        print(di.next())

if __name__ == '__main__':
    sys.exit(test())