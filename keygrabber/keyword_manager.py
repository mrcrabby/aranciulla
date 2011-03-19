#!/usr/bin/python
# -*- coding: UTF-8 -*-

'''
@author: Vincenzo Ampolo <vincenzo.ampolo@gmail.com>
'''
#for unittest
import unittest

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import pymongo
from pymongo.son_manipulator import SONManipulator


Base = declarative_base()

class InstantKeywordMongo(object):
    def __init__(self, keyword, depth):
        self.__dict__.update(dict([(k, v) for k, v in locals().iteritems() if k != 'self']))
    
    def __str__(self):
        return '%s' % (self.keyword)

    class Manipulator(SONManipulator):

        def encode(self, c):
            return {"_type": "InstantKeywordMongo", "keyword": c.keyword, "depth": c.depth}
        
        def decode(self, d):
            assert d["_type"] == "InstantKeywordMongo"
            return InstantKeywordMongo(d["keyword"], d["depth"])
        
        def transform_incoming(self, son, collection):
            for (key, value) in son.items():
              if isinstance(value, InstantKeywordMongo):
                son[key] = self.encode(value)
              elif isinstance(value, dict): # Make sure we recurse into sub-docs
                son[key] = self.transform_incoming(value, collection)
            return son
    
        def transform_outgoing(self, son, collection):
            for (key, value) in son.items():
              if isinstance(value, dict):
                if "_type" in value and value["_type"] == "InstantKeywordMongo":
                  son[key] = self.decode(value)
                else: # Again, make sure to recurse into sub-docs
                  son[key] = self.transform_outgoing(value, collection)
            return son
        
class InstantKeyword(Base):
    __tablename__='instantkeyword'
    keyword = Column(String, primary_key=True)
    depth = Column(Integer)
    place = Column(Integer)
    parent_id = Column(String, ForeignKey('instantkeyword.keyword'))
    parent = relationship("InstantKeyword", uselist=False )
    
    def __init__(self, keyword, depth, place, parent = None):
        self.depth = depth
        self.place = place
        self.parent = parent
        self.keyword = keyword
        
    def __repr__(self):
        return self.__str__()
        
    def __str__(self):
        return 'key:%s, depth:%s, place:%s' % (self.keyword, self.depth, self.place)
        
class KeywordManager():
    '''
    def __init__(self, dictionary, s_eng, until, engine_config):
        self.keywords = list()
        self.dictionary = dictionary
        self.s_eng = s_eng
        self.Error = until
        engine = create_engine(engine_config)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
    '''    
    def __init__(self, dictionary, s_eng, until):
        self.keywords = list()
        self.dictionary = dictionary
        self.s_eng = s_eng
        self.Error = until
        self.connection = pymongo.Connection()
        self.db = self.connection.webkeywords
        self.db.add_son_manipulator(InstantKeywordMongo.Manipulator())
        self.collection = self.db.keywords

        
    def __add_keywords_to_database(self, keywords, depth=0, *args, **kwargs):
        return self.__add_keywords_to_mongo(keywords, depth, *args, **kwargs)
    
    def __add_keywords_to_postgresql(self, keywords, depth=0, *args, **kwargs):
        keys = list()
        for keyword in keywords:
            try:
                self.session.query(InstantKeyword).filter(InstantKeyword.keyword == keyword).one()
            except NoResultFound, e:
                key_entry= InstantKeyword(keyword, depth, keywords.index(keyword))
                self.session.add(key_entry)
                keys.append(key_entry)
        self.session.commit()
        return keys
    
    def __add_keywords_to_mongo(self, keywords, depth, *args, **kwargs):
        key = InstantKeywordMongo(keywords, depth) 
        keys = list()
        for keyword in keywords:
            key_entry= InstantKeywordMongo(keyword, depth)
            self.collection.insert({key_entry.keyword.replace('.', ''):key_entry})
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
        return self.session.query(InstantKeyword).filter(InstantKeyword.depth == depth).all()
        
    def export_keywords(self, *args, **kwargs):
        keywords = self.session.query(InstantKeyword).all()
        print 'keyword, depth, place'
        for key in keywords:
            print '%s, %s, %s' % (key.keyword.encode('utf-8'), key.depth, key.place)
        
    def simpleSearch(self, base='', *args, **kwargs):
        i = 0
        to_expand = list()
        
        to_expand.extend(self.__search_and_add_keywords_to_database(base, i))
        
        while(True):
            try:
                key = base+self.dictionary.next()
            except self.Error:
                print 'finished dictionary - starting expand'
                break
            print 'looking for: '+key
            to_expand.extend(self.__search_and_add_keywords_to_database(key, i))
        
        ist_keys = self.__get_all_keywords(i)
        i = 1
        for keyw in ist_keys:
            self.__search_expand_and_add_keywords_to_database(keyw.keyword, i)
        print 'algorithm finished'
            


#a = InstantKeyword('test', 1, 2)
#session.add(a)
#session.commit()
#print session.query(InstantKeyword).all()

class KeywordManagerTest(unittest.TestCase):
    def test_database(self):
        import settings
        engine = create_engine(settings.engine_config, echo=True)
        Session = sessionmaker(bind=engine)
        session = Session()
        #to create the schema
        Base.metadata.create_all(engine)
        
    

if __name__ == '__main__':
    unittest.main()
        
    
    