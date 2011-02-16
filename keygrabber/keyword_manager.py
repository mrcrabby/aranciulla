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

Base = declarative_base()

      
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
    def __init__(self, dictionary, s_eng, until, engine_config):
        self.keywords = list()
        self.dictionary = dictionary
        self.s_eng = s_eng
        self.Error = until
        engine = create_engine(engine_config)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        
    def __add_keywords_to_database(self, keywords, depth=0, *args, **kwargs):
        keys = list()
        for keyword in keywords:
            try:
                self.session.query(InstantKeyword).filter(InstantKeyword.keyword == keyword).one()
            except NoResultFound, e:
                key_entry= InstantKeyword(keyword, depth, keywords.index(keyword))
                keys.append(key_entry)
        self.session.add_all(keys)
        self.session.commit()
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
        
    def export_keywords(self, *args, **kwargs):
        keywords = self.session.query(InstantKeyword).all()
        print 'keyword, depth, place'
        for key in keywords:
            print '%s, %s, %s' % (key.keyword.encode('utf-8'), key.depth, key.place)
        
    def simpleSearch(self, base='', *args, **kwargs):
        i = 0
        to_expand = list()
        while(True):
            try:
                key = base+self.dictionary.next()
            except self.Error:
                print 'finished dictionary - starting expand'
                i = 1
                for keyw in to_expand:
                    self.__search_expand_and_add_keywords_to_database(keyw, i)
                break
            print 'looking for: '+key
            to_expand.extend(self.__search_and_add_keywords_to_database(key, i))
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
        
    
    