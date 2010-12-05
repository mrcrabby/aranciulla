#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Options:

-f filter keywords if present in the page
-m gimme more info
-e do an EXACT research instead of BROAD
-u num : print at maximum num entries
 
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''
import sys
import os
import getopt
import subprocess
import codecs
import sys
(head, tail) = os.path.split(os.path.abspath(os.path.dirname(__file__)))
sys.path.append(head)
sys.path.append(os.path.join(head,tail))
from aralib.google import Google
from aralib.keyword import KeywordManager


import pdb

    
def main(argv=None):
    if argv is None:
       argv = sys.argv
    
    opts, extraparams = getopt.gnu_getopt(argv[1:], "hvfmeu:", ["help", "--filter", "--more", '--exact', '--upper-bound='])
    
    verbose = False
    more_info = False
    filter = False
    filter_url =  u'http://aranzulla.tecnologia.virgilio.it/s/'
    upper_bound = 1000
    lower_bound = -1
    mode = 'BROAD'
    
    google = Google()
    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-u", "--upper-bound"):
            upper_bound = int(a)
        elif o in ("-l", "--lower-bound"):
            lower_bound = int(a)
        elif o in ("-n", "--num-words"):
            num_words = int(a)
        elif o in ("-f", "--filter"):
            filter = True
        elif o in ("-h", "--help"):
            print __doc__
            sys.exit(0)
        elif o in ("-m", "--more"):
            more_info = True
        elif o in ("-e", "--exact"):
            mode = 'EXACT'
        else:
            assert False, "UnhandledOption"
                     
    for keyword in extraparams:
        km = KeywordManager(keyword)
        keywords = google.getAdwordsKeywords(keyword, mode)
        km.importStructuredKeywords(keyword, keywords)
        km.removeUncleanKeywords()
        if mode == 'BROAD':
            km.removeEqualGlobalsAndRegionals()
        km.sort('regional_score')
            
        print 'Computing results...'
        doc = km.genXml(lower_bound, upper_bound)
        f = codecs.open(os.path.join('output', keyword+'.xml'), 'w', 'utf-8')
        f.write(doc.toprettyxml(indent='  '))
        f.close()
        
        if filter:
            print 'Computing filtered results...'
            doc = km.genXml(lower_bound, upper_bound, filter_url)
            f = codecs.open(os.path.join('output', keyword+'-filtered.xml'), 'w','utf-8')
            f.write(doc.toprettyxml(indent='  '))
            f.close()
            #make diff
            subprocess.Popen(['diff -Naru ' +os.path.join('output', keyword+'.xml')+ ' ' + os.path.join('output', keyword+'-filtered.xml') + ' > ' + os.path.join('output', keyword+'-filtered.diff') ], shell=True)
        
        #save everything
        f = codecs.open(os.path.join('output', keyword+'.txt'), 'w', 'utf-8')
        if more_info:
            f.writelines([unicode(obj)+'\n' for obj in km.getKeywordEntries()])
        else:
            f.writelines([unicode(obj.keyword)+'\n' for obj in km.getKeywordEntries()])
        f.close()            
        
    print 'Program terminates correctly'
    return 0
            
            
if __name__ == '__main__':
    sys.exit(main())
