#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''
#for unittest
import unittest

import pymongo

class InstantKeywordMongo(object):
    def __init__(self, keyword, depth):
        self.keyword = keyword
        self.depth = depth
    
    def __str__(self):
        return '%s' % (self.keyword)
    
    def to_dict(self):
        d = dict()
        d['keyword'] = self.keyword
        d['depth'] = self.depth
        return d

            
class KeywordManager():    
    def __init__(self, dictionary, s_eng, until):
        self.keywords = list()
        self.dictionary = dictionary
        self.s_eng = s_eng
        self.Error = until
        self.connection = pymongo.Connection()
        self.db = self.connection.webkeywords
        self.collection = self.db.keywords
        self.collection.ensure_index('keyword')

        
    def __add_keywords_to_database(self, keywords, depth=0, *args, **kwargs):
        return self.__add_keywords_to_mongo(keywords, depth, *args, **kwargs)
    
    def __add_keywords_to_mongo(self, keywords, depth, *args, **kwargs):
        key = InstantKeywordMongo(keywords, depth) 
        keys = list()
        for keyword in keywords:
            result = self.collection.find_one({'keyword':keyword})
            if result is None:
                key_entry= InstantKeywordMongo(keyword, depth)
                self.collection.insert(key_entry.to_dict())
                keys.append(key_entry)
        return keys       
    
    def __search_and_add_keywords_to_database(self, key, depth=0, *args, **kwargs):
        r_search = self.s_eng.search(key)
        return self.__add_keywords_to_database(r_search, depth)
    
    def __search_expand_and_add_keywords_to_database(self, keyword, depth=0, *args, **kwargs):
        '''
        Expand and add all the keywords found based on a keyword
        '''
        r_search = self.s_eng.expand(keyword)
        return self.__add_keywords_to_database(r_search, depth)
    
    def __get_all_keywords(self, depth=0, *args, **kwargs):
        return self.collection.find({'depth': depth})
        
    def export_keywords(self, *args, **kwargs):
        keywords = self.collection.find()
        print 'keyword, depth'
        for key in keywords:
            print '%s, %s' % (key.get('keyword'), key.get('depth'))
        
    def simpleSearch(self, base='', *args, **kwargs):
        i = 0
        to_expand = list()
        '''
        to_expand.extend(self.__search_and_add_keywords_to_database(base, i))
        
        while(True):
            try:
                key = base+self.dictionary.next()
            except self.Error:
                print 'finished dictionary - starting expand'
                break
            print 'looking for: '+key
            to_expand.extend(self.__search_and_add_keywords_to_database(key, i))
        '''
        ist_keys = [InstantKeywordMongo(x.get('keyword'), x.get('depth')) for x in self.__get_all_keywords(i)]
        i = 1
        for keyw in ist_keys:
            self.__search_expand_and_add_keywords_to_database(keyw.keyword, i)
        print 'algorithm finished'
            

class KeywordManagerTest(unittest.TestCase):
    def test_mongo_class(self):
        a = InstantKeywordMongo('test',0)
        print a.to_dict()
        km = KeywordManager(None, None, None)
        print km.collection.insert(a)
        
    def test_export(self):
        km = KeywordManager(None, None, None)
        km.export_keywords()
    

if __name__ == '__main__':
    unittest.main()