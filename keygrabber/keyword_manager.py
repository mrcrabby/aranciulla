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
from string import ascii_lowercase
import itertools


logging.basicConfig(level=logging.DEBUG)

log = logging.getLogger('keywordManager')
log.addHandler(logging.FileHandler('/tmp/keygrabber.log', 'w'))

class InstantKeywordMongo(object):
    def __init__(self, keyword=None, parent=None, category=None, level=None, dicts=None, depth=None, place=None, dbplace=None, **kwargs):
        self.keyword = keyword
        self.parent = parent
        self.category = category
        self.level = level
        self.dicts = dicts
        self.depth = depth
        self.place = place
        self.dbplace = dbplace
        self.has_child = False
        self._id = None
        self.fields = ['keyword', 'level', 'dicts', 'depth', 'place', 'dbplace', 'category', 'parent', 'has_child', '_id']
    def __str__(self):
        return 'keyword: %s, parent: %s, dicts: %s, level: %s, depth: %s, dbplace: %s, place: %s' % (self.keyword, self.parent, self.dicts, self.level, self.depth, self.dbplace, self.place)
    
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
		self.collection.ensure_index([('level',pymongo.ASCENDING), ('dicts', pymongo.ASCENDING), ('depth', pymongo.ASCENDING), ('dbplace', pymongo.ASCENDING)])

        
	def __add_keywords_to_database(self, keywords=None, parent_k=None, **kwargs):
		return self.__add_keywords_to_mongo(keywords, parent_k, **kwargs)
	
	def __add_keywords_to_mongo(self, keywords=None, parent_k=None, **kwargs):
		keys = list()
		d_lev = None
		expans = kwargs.get('expanded_list')
		if expans is not None:
			d_lev = dict()
			keywords = list() if keywords is None else keywords
			for key,lev in expans:
				keywords.append(key)
				d_lev[key]=lev
		if parent_k is None:
			parent_k = InstantKeywordMongo('parent', None, None, 0, 0, 0, 0)
		for keyword in keywords:
			result = self.collection.find_one({'keyword':keyword})
			if result is None:
				key_entry= InstantKeywordMongo(keyword, parent_k.keyword, parent_k.category, d_lev[keyword] if d_lev else parent_k.level, parent_k.dicts, parent_k.depth, keywords.index(keyword)+1, len(keys)+1)
				key_entry._id = self.collection.insert(key_entry.to_dict())
				if parent_k._id is not None and parent_k.has_child is False:
					parent_k.has_child = True
					self.collection.save(parent_k.to_dict())
				keys.append(key_entry)
		return keys       
    
	def order_keywords(self, *args, **kwargs):
		return self.fast_order()
	    
	def export_keywords(self, *args, **kwargs):
		keywords = self.db.orderedkeys.find()
		print('keyword, dicts, level, depth, dbplace')
		for key in keywords:
			print('%s, %s, %s, %s, %s' % (key.get('keyword'), key.get('dicts'), key.get('level'), key.get('depth'), key.get('dbplace')))
	
	def drop_database(self):
		self.collection.drop()
		
	def create_orderedkeys_collection(self, inst_list):
		#add index
		log.info('adding index')
		for i, key in enumerate(inst_list):
			key['index']=i 
		#save to orderedkeys collection
		self.db.orderedkeys.drop()
		log.info('adding ordered keys :'+str(len(inst_list)))
		a = self.db.orderedkeys.insert(inst_list)
		print(len(a))
		return inst_list
		
	
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
			keys_got = list()
			for k, lev in r_search:
				keys_got.append((k, lev))
			keys.extend(self.__add_keywords_to_database(parent_k=mkey, expanded_list=keys_got))       
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
		log.warning('Ordering and publishing')
		keywords = self.order_keywords()
		self.create_orderedkeys_collection(keywords)
		
	def fast_order(self):
		log.warning('Start fast ordering')
		
		inst_list = list()
		cursors = list()
		wrong_list = list()
		
		def _update_threshold(level = 5, depth =4, dbplace=10):	
			m_dicts = 1
			m_level = 0
			m_depth = 0
			m_dbplace = 1
			
			yield (m_dicts, m_level, m_depth, m_dbplace)
			
			while True:
				m_dbplace = m_dbplace + 1
				if m_dbplace > dbplace:
					m_depth = m_depth +1
					m_dbplace = 1
				if m_depth > depth:
					m_level = m_level + 1
					m_depth = 0
					m_dbplace = 0
				if m_level > level:
					m_dicts = m_dicts +1
					m_level = 0
					m_depth = 0
					m_dbplace = 0
				yield (m_dicts, m_level, m_depth, m_dbplace)
		
		root = self.collection.find_one(dict(dicts=0, parent=None))
		max_dict = self.collection.find().sort([('dicts',pymongo.DESCENDING),])[0].get('dicts')
		for (dicts, level, depth, dbplace) in _update_threshold():
			log.info("threashold:"+str(dicts)+" "+str(level)+" "+str(depth)+" "+str(dbplace))
			for letter in ascii_lowercase:
				items = [item for item in self.collection.find(dict(keyword=re.compile('^'+root.get('keyword')+' '+letter), dicts=dicts, level=level, depth=depth, dbplace=dbplace))]
				if len(items) > 0:
					inst_list.extend(items)
			log.info("successfully ordered :"+str(len(inst_list)))
			if dicts >= max_dict:
					break
		return inst_list
			
		
	def order_and_publish(self):
		log.warning('Starting ordering')
		inst_list = list()
		res = list()
		res_index = list()
		root = self.collection.find_one(dict(dicts=0, parent=None))
		ten_items = self.collection.find(dict(parent=root.get('keyword'), dicts=1))[:10]
		ten_items_list = [x for x in ten_items]
		inst_list.extend(ten_items_list)
		max_items = 0
		for letter in ascii_lowercase:
			items = self.collection.find(dict(keyword=re.compile(root.get('keyword')+' '+letter))).sort([('dicts', pymongo.ASCENDING), ('level', pymongo.ASCENDING), ('depth', pymongo.ASCENDING), ('dbplace', pymongo.ASCENDING), ('keyword', pymongo.ASCENDING)])
			n_items = items.count()
			items.batch_size(1000)
			res.append(items)
			res_index.append(0)
			max_items = n_items if n_items >= max_items else max_items
		log.info('cursors built')	
		
		def smart_ordering(cursors, **kwargs):			
			
			cursors_indexes = [0 for i in cursors]
			base_list = kwargs.get('base_list', list())
			dicts = 1
			level = 0
			depth = 0
			dbplace = 1
			
			skipped_counter = [0, 0, 0, 0]
				
			def continue_iteration(cursors):
				return False if all([cursor.count() <= cursors_indexes[cursors.index(cursor)] for cursor in cursors]) else True
				
			def __update_counter(counter, value):
				if counter >= 26:
					value = value +1 
					return 0, value
				else:
					return counter + 1, value
			
			start_from_a = False
			while continue_iteration(cursors):
				for cursor in cursors:
					c_index = cursors.index(cursor)
					if start_from_a:
						if c_index != 0:
							break
						else:
							start_from_a = False
					index = cursors_indexes[c_index]
					while cursor.count() > index:
						if cursor[index] in base_list:
							index=index+1
						else:
							key = cursor[index]
							log.info('selected key ' + key.get('keyword'))
							log.info('counters%s' % (str(skipped_counter),))
							log.info('threshold: dicts: %s level: %s depth: %s dbplace: %s' % (dicts, level, depth, dbplace))
							if key.get('dicts') <= dicts:
								#skipped_counter[0] = 0
								if key.get('level') <= level: 
									#skipped_counter[1] = 0
									if key.get('depth') <= depth:
										#skipped_counter[2] = 0
										if key.get('dbplace') <= dbplace:
											#skipped_counter[3] = 0
											print('added')
											inst_list.append(key)
											cursors_indexes[c_index] = index + 1
											print('updating index: ', cursors_indexes[c_index])
											yield key
										else:
											skipped_counter[3], dbplace = __update_counter(skipped_counter[3], dbplace) 
											if skipped_counter[3] == 0:
												start_from_a = True
									else:
										skipped_counter[2], depth = __update_counter(skipped_counter[2], depth) 
										if skipped_counter[2] == 0:
											dbplace = 0
											start_from_a = True
								else:
									skipped_counter[1], level = __update_counter(skipped_counter[1], level)
									if skipped_counter[1] == 0:
										depth = 0
										dbplace = 0
										start_from_a = True
							else:
								skipped_counter[0], dicts = __update_counter(skipped_counter[0], dicts)
								if skipped_counter[0] == 0:
									depth = 0
									level = 0
									dbplace = 0
									start_from_a = True
							break
		
		inst_list.extend([i for i in smart_ordering(res, base_list=inst_list)])
		
		#add index
		log.info('do ordering')
		for i, key in enumerate(inst_list):
			key['index']=i 
		#save to orderedkeys collection
		self.db.orderedkeys.drop()
		self.db.orderedkeys.insert(inst_list)
		return []
		return inst_list
			
						
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
