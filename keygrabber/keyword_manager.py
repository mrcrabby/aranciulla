#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''
#for unittest
import unittest
import pymongo
from google import Google, max_answers
from dictionary_generator import SmartDict

class InstantKeywordMongo(object):
    def __init__(self, keyword=None, parent=None, category=None, level=None, dicts=None, depth=None, place=None, **kwargs):
        self.keyword = keyword
        self.parent = parent
        self.category = category
        self.level = level
        self.dicts = dicts
        self.depth = depth
        self.place = place
        self.has_child = False
        self._id = None
        self.fields = ['keyword', 'level', 'dicts', 'depth', 'place', 'category', 'parent', 'has_child', '_id']
    def __str__(self):
        return '%s' % (self.keyword)
    
    def to_dict(self):
        d = dict()
        for field in self.fields:
        	if getattr(self, field) is not None:
        		d[field] = getattr(self, field)
        return d

            
class KeywordManager():    
    def __init__(self, dictionary, s_eng):
        self.keywords = list()
        self.dictionary = dictionary
        self.s_eng = s_eng
        self.connection = pymongo.Connection()
        self.db = self.connection.webkeywords
        self.collection = self.db.keywords
        self.collection.ensure_index('keyword')

        
    def __add_keywords_to_database(self, keywords, parent_k, **kwargs):
        return self.__add_keywords_to_mongo(keywords, parent_k, **kwargs)
    
    def __add_keywords_to_mongo(self, keywords, parent_k, **kwargs):
        keys = list()
        for keyword in keywords:
            result = self.collection.find_one({'keyword':keyword})
            if result is None:
                key_entry= InstantKeywordMongo(keyword, parent_k.keyword, parent_k.category, parent_k.level, parent_k.dicts, parent_k.depth, keywords.index(keyword)+1)
                key_entry._id = self.collection.insert(key_entry.to_dict())
                if parent_k.has_child is False:
                	parent_k.has_child = True
                	self.collection.save(parent_k.to_dict())
                keys.append(key_entry)
        return keys       
    
    def __search_and_add_keywords_to_database(self, mkey, dictionary, *args, **kwargs):
        r_search = self.s_eng.search(mkey.keyword)
        if len(r_search) < max_answers:
            dictionary.jump()
        return self.__add_keywords_to_database(r_search, mkey)
    
    def __search_expand_and_add_keywords_to_database(self, mkey, *args, **kwargs):
        '''
        Expand and add all the keywords found based on a keyword
        '''
        r_search = self.s_eng.expand(mkey.keyword, mkey.level)
        keys = list()
        for k, lev in r_search:
            mkey.level = lev
            keys.extend(self.__add_keywords_to_database(k, mkey))       
        return keys
        
    def export_keywords(self, *args, **kwargs):
        keywords = self.collection.find()
        print('keyword, depth')
        for key in keywords:
            print('%s, %s' % (key.get('keyword'), key.get('depth')))
    
    def drop_database(self):
        self.collection.drop()
    '''    
    def simpleSearch(self, base='', *args, **kwargs):
        i = 0
        to_expand = list()
        to_expand.extend(self.__search_and_add_keywords_to_database(base, i))
        
        while(True):
            try:
                key = base+self.dictionary.next()
            except self.Error:
                print('finished dictionary - starting expand')
                break
            print('looking for: '+key)
            to_expand.extend(self.__search_and_add_keywords_to_database(key, i))
        
        ist_keys = [InstantKeywordMongo(x.get('keyword'), x.get('depth')) for x in self.__get_all_keywords(i)]
        i = 1
        for keyw in ist_keys:
            self.__search_expand_and_add_keywords_to_database(keyw.keyword, i)
        print('algorithm finished')
    '''
    
    def not_so_simple_search(self, base='', **kwargs):
        level = 0
        dicts = 0
        to_expand = list()
        #first of all look for keywords with just the BASE
        base_k = InstantKeywordMongo(base, None, None, level, dicts, 0)
        to_expand.extend(self.__search_and_add_keywords_to_database(base_k, self.dictionary))
        
        dicts = dicts + 1
        for word in self.dictionary.get():
            print('looking for: '+base_k.keyword+word)
            key = InstantKeywordMongo(base_k.keyword+word, base_k.keyword, None, level, dicts, len(word))
            to_expand.extend(self.__search_and_add_keywords_to_database(key, self.dictionary))
        
        print('expanding')
        ist_keys = [InstantKeywordMongo(x.get('keyword'), x.get('parent'), x.get('category'), x.get('level'), x.get('dicts'), x.get('depth'), x.get('place')) for x in self.collection.find({'level': 0})]
        for keyw in ist_keys:
            self.__search_expand_and_add_keywords_to_database(keyw)
                

class KeywordManagerTest(unittest.TestCase):
    
    def test_mongo_class(self):
        a = InstantKeywordMongo('test',0)
        print(a.to_dict())
        km = KeywordManager(None, None, None)
        print(km.collection.insert(a))
        
    def test_export(self):
        km = KeywordManager(None, None, None)
        km.export_keywords()
    

if __name__ == '__main__':
    unittest.main()