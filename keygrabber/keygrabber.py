#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''

import sys
import os
import getopt
import codecs


from google import Google
from keyword_manager import KeywordManager
from dictionary_generator import Dictionary, RangeError
import settings

    
def main(argv=None):
    if argv is None:
       argv = sys.argv
    
    opts, extraparams = getopt.gnu_getopt(argv[1:], "hve", ["help", 'export'])
    
    verbose = False
    export = False    
    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif o in ("-e", "--export"):
            export = True
        else:
            assert False, "UnhandledOption"

    #begin
    google = Google(settings.proxy)
    di = Dictionary('a')
    km = KeywordManager(di, google, RangeError)
    
    if export:
        km.export_keywords()
        return 0
    
    km.simpleSearch(base='come ')
    
    return 0
            
if __name__ == '__main__':
    sys.exit(main())