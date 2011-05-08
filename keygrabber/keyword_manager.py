#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''
#for unittest
import unittest
import pymongo
import logging
from google import Google, max_answers
from dictionary_generator import SmartDict
import re

logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('keywordManager')
log.addHandler(logging.FileHandler('/tmp/keygrabber.log', 'w'))

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
		self.s_eng = s_eng
		self.connection = pymongo.Connection()
		self.db = self.connection.webkeywords
		self.collection = self.db.crawler
		self.collection.ensure_index('keyword')
		self.collection.ensure_index([('level',pymongo.ASCENDING), ('dicts', pymongo.ASCENDING), ('depth', pymongo.ASCENDING), ('place', pymongo.ASCENDING)])

        
	def __add_keywords_to_database(self, keywords, parent_k, **kwargs):
		return self.__add_keywords_to_mongo(keywords, parent_k, **kwargs)
	
	def __add_keywords_to_mongo(self, keywords, parent_k, **kwargs):
		keys = list()
		level = kwargs.get('level')
		if parent_k is None:
			parent_k = InstantKeywordMongo('parent', None, None, 0, 0, 0, 0)
		for keyword in keywords:
			result = self.collection.find_one({'keyword':keyword})
			if result is None:
				key_entry= InstantKeywordMongo(keyword, parent_k.keyword, parent_k.category, level if level else parent_k.level, parent_k.dicts, parent_k.depth, keywords.index(keyword)+1)
				key_entry._id = self.collection.insert(key_entry.to_dict())
				if parent_k._id is not None and parent_k.has_child is False:
					parent_k.has_child = True
					self.collection.save(parent_k.to_dict())
				keys.append(key_entry)
		return keys       
    
	    
	def export_keywords(self, *args, **kwargs):
		self.order_and_publish()
		'''
		keywords = self.collection.find()
		print('keyword, depth')
		for key in keywords:
			print('%s, %s' % (key.get('keyword'), key.get('depth')))
		'''
	
	def drop_database(self):
		self.collection.drop()
	
	def not_so_simple_search(self, base='', **kwargs):
		level = 0
		dicts = 0
		to_start_dict = list()
						
		def expand(mkey, *args, **kwargs):
			'''
			Expand and add all the keywords found based on a keyword
			'''
			#TODO: split the extended in multiple keywords
			r_search = self.s_eng.expand(mkey.keyword, mkey.level)
			keys = list()
			for k, lev in r_search:
				keys.extend(self.__add_keywords_to_database([k], mkey, level=lev))       
			return keys
				
		ilist=list()	
		#first of all look for keywords with just the BASE
		base_k = InstantKeywordMongo(base, None, None, level, dicts, 0)
		base_k._id = self.collection.insert(base_k.to_dict())
		to_start_dict.append(base_k)			
			
		for key in to_start_dict:
			dicts = dicts + 1
			d = SmartDict(size=4)
			log.warning('starting dict for ='+key.keyword) 
			for word in d.get():
				ilist=list()
				log.debug('SEARCHING for ='+key.keyword+' '+word)
				key = InstantKeywordMongo(key.keyword, key.parent, None, level, dicts, len(word))
				r_search = self.s_eng.search(key.keyword+' '+word)
				if len(r_search) < max_answers:
					d.jump()
				keyws = self.__add_keywords_to_database(r_search, key)
				log.debug('ADDED into the database ='+str([x.keyword for x in keyws]))
				ilist.extend(keyws)
				#evaluate(keyws)
				if len(r_search) == max_answers:
					log.debug('starting expansion results == 10')
					for keyw in keyws:
						#TODO: valuate if i should add keyw into to_start_dict
						log.debug('expanding ='+keyw.keyword)
						exp_ress = expand(keyw)
						log.debug('expanded and saved into database ='+str([x.keyword for x in exp_ress]))
						ilist.extend(exp_ress)
				for x in ilist:
					log.debug('Evaluating ='+x.keyword)
					if self.collection.find(dict(keyword=re.compile(re.escape(x.keyword)))).count() >= max_answers and all(y.keyword != x.keyword for y in to_start_dict):
						to_start_dict.append(x)
						log.debug('ADDED to the list of dict ='+x.keyword)
		log.warning('Algorithm Finished')
		
	def order_and_publish(self):
		inst_list = list()
		res = list()
		root = self.collection.find_one(dict(dicts=0, parent=None))
		ten_items = self.collection.find(dict(parent=root.get('keyword'), dicts=1))[:10]
		ten_items_list = [x for x in ten_items]
		inst_list.extend(ten_items_list)
		max_items = 0
		for letter in ascii_lowercase:
			items = self.collection.find(dict(keyword=re.compile(root.get('keyword')+' '+letter))).sort([('dicts', pymongo.ASCENDING), ('level', pymongo.ASCENDING), ('depth', pymongo.ASCENDING), ('place', pymongo.ASCENDING)])
			n_items = items.count()
			items.batch_size(1000)
			res.append(items)
			max_items = n_items if n_items >= max_items else max_items
		for n in range(max_items):
			for r in res:
				if r.count() > n and r[n] not in ten_items_list:
					inst_list.append(r[n])
		print(inst_list)
						
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
