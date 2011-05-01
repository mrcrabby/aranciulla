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
from dictionary_generator import SmartDict
import settings
import string

    
def main(argv=None):
    if argv is None:
       argv = sys.argv
    
    opts, extraparams = getopt.gnu_getopt(argv[1:], "hved", ["help", 'export', 'drop'])
    
    verbose = False
    export = False
    drop = False    
    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            print(__doc__)
            sys.exit(0)
        elif o in ("-e", "--export"):
            export = True
        elif o in ("-d", "--drop"):
            drop = True
        else:
            assert False, "UnhandledOption"

    #begin
    google = Google(settings.proxy)
    di = SmartDict(size=4)
    km = KeywordManager(di, google)
    
    if export:
        km.export_keywords()
        return 0
    
    if drop:
        km.drop_database()
        return 0
    
    km.not_so_simple_search(base='come scaricare')
    
    return 0
            
if __name__ == '__main__':
    sys.exit(main())
