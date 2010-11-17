#!/usr/bin/python
# -*- coding: UTF-8 -*-
'''
Options:

-u num | --upper-bound num : print at max num nephews
-l num | --lower-bound num : print at min num nephews
-n num | --num-words : keywords with len n
 
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''
import sys
import os
import getopt
import subprocess
import codecs



import pdb

    
def main(argv=None):
    if argv is None:
       argv = sys.argv
    
    opts, extraparams = getopt.gnu_getopt(argv[1:], "hvu:l:n:f", ["help", "upper-bound=", "lower-bound", "num-words", "--filter"])
    
    verbose = False
    more_info = False
    filter = False
    filter_url =  u'http://aranzulla.tecnologia.virgilio.it/s/'
    upper_bound = 1000
    lower_bound = 1
    num_words = 3
    
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
        else:
            assert False, "UnhandledOption"
                     
    for keyword in extraparams:
        keyword_entries = []
        #keywords = search_with_trellian(keyword)
        __get_google_keywords(keyword)
        return 
        keywords = filter_bannedchars(keywords)
        
        print 'Cleaning duplicates'
        #B
        for key in keywords:
            norm_key = genKey(keyword, key)
            if len(key.split()) > num_words:
                continue
            #C
            duplicate = False
            for entry in keyword_entries:
                if entry.key == norm_key:
                    duplicate = True
            if(not duplicate):
                keyword_entries.append(KeywordEntry(key, norm_key))
        
        
        
        #grouping
        k_w_copy = list(keyword_entries)
        
        for obj in k_w_copy:
            if obj.keyword == keyword:
                k_w_copy.pop(k_w_copy.index(obj))
        
        for obj in k_w_copy:
            for obj2 in k_w_copy:
                if relation(obj.key, obj2.key) and not obj2.selected:
                    obj.children.append(k_w_copy[k_w_copy.index(obj2)])
                    obj2.selected = True
                    obj.selected = True
            
        print 'Computing results...'
        doc = __gen_xml(keyword, k_w_copy, lower_bound, upper_bound)
        f = codecs.open(os.path.join('output', keyword+'.xml'), 'w', 'utf-8')
        f.write(doc.toprettyxml(indent='  '))
        f.close()
        
        if filter:
            print 'Computing filtered results...'
            doc = __gen_xml(keyword, k_w_copy, lower_bound, upper_bound, filter_url)
            f = codecs.open(os.path.join('output', keyword+'-filtered.xml'), 'w','utf-8')
            f.write(doc.toprettyxml(indent='  '))
            f.close()
            #make diff
            subprocess.Popen(['diff -Naru ' +os.path.join('output', keyword+'.xml')+ ' ' + os.path.join('output', keyword+'-filtered.xml') + ' > ' + os.path.join('output', keyword+'-filtered.diff') ], shell=True)
        
        #save everything
        f = codecs.open(os.path.join('output', keyword+'.txt'), 'w', 'utf-8')
        if more_info:
            f.writelines([unicode(obj)+'\n' for obj in keyword_entries])
        else:
            f.writelines([unicode(obj.keyword)+'\n' for obj in keyword_entries])
        f.close()            
        
    print 'Program terminates correctly'
    return 0
            
            
if __name__ == '__main__':
    sys.exit(main())
