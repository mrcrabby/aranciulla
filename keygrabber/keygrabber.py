#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''

import sys
import os
import getopt

from google import Google
from keyword_manager import KeywordManager
from dictionary_generator import Dictionary, RangeError
import settings

    
def main(argv=None):
    if argv is None:
       argv = sys.argv
    
    opts, extraparams = getopt.gnu_getopt(argv[1:], "hv", ["help"])
    
    verbose = False    
    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        else:
            assert False, "UnhandledOption"

    #begin
    google = Google(settings.proxy)
    di = Dictionary('a')
    km = KeywordManager(di, google, RangeError, settings.engine_config)
    
    km.simpleSearch()
    
    return 0
            
if __name__ == '__main__':
    sys.exit(main())