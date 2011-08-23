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


logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(message)s')

log = logging.getLogger('keywordManager')
hdlr = logging.FileHandler('/tmp/keygrabber.log', 'w')
formatter = logging.Formatter('%(asctime)s %(message)s')
hdlr.setFormatter(formatter)
log.addHandler(hdlr)

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
        self.global_searches = None
        self.regional_searches = None
        self.fields = ['keyword', 'level', 'dicts', 'depth', 'place', 'dbplace', 'category', 'parent', 'has_child', '_id', 'global_searches', 'regional_searches']
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
		log.debug('Adding keywords to database part')
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
				log.debug('keyword NOT found in database: '+ keyword)
				key_entry= InstantKeywordMongo(keyword, parent_k.keyword, parent_k.category, d_lev[keyword] if d_lev else parent_k.level, parent_k.dicts, parent_k.depth, keywords.index(keyword)+1, len(keys)+1)
				key_entry._id = self.collection.insert(key_entry.to_dict())
				if parent_k._id is not None and parent_k.has_child is False:
					parent_k.has_child = True
					self.collection.save(parent_k.to_dict())
				keys.append(key_entry)
			else:
				log.debug('keyword found in database: '+ keyword)
		return keys       
    
	def order_keywords(self, *args, **kwargs):
		return self.fast_order()
	    
	def export_keywords(self, *args, **kwargs):
		keywords = self.db.orderedkeys.find()
		print('keyword, index, dicts, level, depth, dbplace')
		for key in keywords:
			print('%s, %s, %s, %s, %s, %s' % (key.get('keyword'), key.get('index'), key.get('dicts'), key.get('level'), key.get('depth'), key.get('dbplace')))
	
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
		self.db.orderedkeys.ensure_index('index')
		print(len(a))
		return inst_list
		
	
	def not_so_simple_search(self, base='', **kwargs):
		level = 0
		dicts = 0
		to_start_dict = list()
		to_start_dict_removed = set()
		already_done_dicts = set()
		to_start_dict_less_of_ten_results = set()
						
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
		
		self.collection.drop()
		ilist=list()	
		#first of all look for keywords with just the BASE
		base_k = InstantKeywordMongo(base, None, None, level, dicts, 0)
		base_k._id = self.collection.insert(base_k.to_dict())
		to_start_dict.append(base_k)			
		
		for key in to_start_dict:
			if key.keyword in already_done_dicts:
				log.warning('found keyword which has already been processed... skipping ' + key.keyword)
				continue
			if key.keyword in to_start_dict_less_of_ten_results:
				log.warning('this keyword has been removed... skipping '+ key.keyword)
				continue
				
			dicts = dicts + 1
			d = SmartDict(size=4)
			log.warning('starting dict for ='+key.keyword) 
			already_done_dicts.add(key.keyword)
			for word in d.get():
				ilist=list()
				log.debug('SEARCHING for ='+key.keyword+' '+word)
				key = InstantKeywordMongo(key.keyword, key.parent, None, level, dicts, len(word))
				r_search = self.s_eng.search(key.keyword+' '+word)
				keyws = self.__add_keywords_to_database(r_search, key)
				for x in keyws:
					log.debug('ADDED into the database: '+x.keyword)
				ilist.extend(keyws)
				if len(r_search) < max_answers:
					d.jump()
					log.debug('reached < 10 answers and SmartDict word is '+word)
					#key_to_check = key.keyword+' '+word+' ' if word != '' else key.keyword+' '
					if word == '':
						key_to_check = key.keyword+' '
						for x in to_start_dict:
							if x.keyword.startswith(key_to_check) and x.keyword not in to_start_dict_less_of_ten_results:
								log.debug('removing '+x.keyword+' from the list_of_dict')
								to_start_dict_less_of_ten_results.add(x.keyword)
					continue
				
				
				log.debug('starting expansion results >= 10')
				for keyw in keyws:
					#TODO: valuate if i should add keyw into to_start_dict
					log.debug('expanding :'+keyw.keyword)
					exp_ress = expand(keyw)
					log.debug('Len of expanded and added to database keywords is '+str(len(exp_ress)))
					ilist.extend(exp_ress)
					
				for x in ilist:
					log.debug('Evaluating :'+x.keyword)
					'''
						Adding multiple dicts support
						Add a keyword to the list of keywords to start in any case
					'''
					keyword = x.keyword[len(base_k.keyword):]
					log.debug('decomposing: '+ x.keyword)
					past_words = ''
					for word in keyword.split()[:-1]:
						possible_keyword = base_k.keyword + past_words +' '+ word
						if all(y.keyword != possible_keyword for y in to_start_dict) and not any(possible_keyword.startswith(x+' ') for x in to_start_dict_removed) and possible_keyword not in to_start_dict_removed and possible_keyword not in already_done_dicts:
							k = InstantKeywordMongo(possible_keyword, None, None, 0, 0, 0)
							k._id = self.collection.insert(k.to_dict())
							to_start_dict.append(k)
							log.debug('ADDED to the list of dict :'+k.keyword)
						past_words = past_words + ' ' + word
								
					if self.collection.find(dict(keyword=re.compile(re.escape(x.keyword)))).count() >= max_answers:
						if all(y.keyword != x.keyword for y in to_start_dict) and x.keyword not in already_done_dicts:
							to_start_dict.append(x)
							log.debug('ADDED to the list of dict :'+x.keyword)
					else:
						to_start_dict_removed.add(x.keyword)
						log.debug('added to the list of to_start_dict_removed '+ x.keyword)
							
		log.warning('Algorithm Finished')
		log.warning('Ordering and publishing')
		keywords = self.order_keywords()
		self.create_orderedkeys_collection(keywords)
		
	def fast_order(self):
		'''
		Algorithm which creates index ffor the keywords based on the values got from the crawler
		'''
		log.warning('Start fast ordering')
		
		inst_list = list()
		cursors = list()
		wrong_list = list()
		
		def _update_threshold(dicts= 100, level = 7, depth =4, dbplace=10):	
			m_dicts = 1
			m_level = 0
			m_depth = 0
			m_dbplace = 1
			
			yield (m_dicts, m_level, m_depth, m_dbplace)
			
			while m_dicts < dicts:
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
		max_dicts = self.collection.find().sort([('dicts',pymongo.DESCENDING),])[0].get('dicts')
		max_level = self.collection.find().sort([('level',pymongo.DESCENDING),])[0].get('level')
		max_depth = self.collection.find().sort([('depth',pymongo.DESCENDING),])[0].get('depth')
		max_dbplace = self.collection.find().sort([('dbplace',pymongo.DESCENDING),])[0].get('dbplace')

		for (dicts, level, depth, dbplace) in _update_threshold(max_dicts, max_level, max_depth, max_dbplace):
			log.info("threashold:"+str(dicts)+" "+str(level)+" "+str(depth)+" "+str(dbplace))
			for letter in ascii_lowercase:
				items = [item for item in self.collection.find(dict(keyword=re.compile('^'+root.get('keyword')+' '+letter), dicts=dicts, level=level, depth=depth, dbplace=dbplace))]
				if len(items) > 0:
					inst_list.extend(items)
			log.info("successfully ordered :"+str(len(inst_list)))
		return inst_list
			
		
	def order_and_publish(self):
		'''
		deprecated function
		Perform a fast and incomplete order
		'''
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
