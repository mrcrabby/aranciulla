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
        engine = create_engine(engine_config, echo=True)
        self.Session = sessionmaker(bind=engine)
        self.session = self.Session()
        
    def __search_and_add_keywords_to_database(self, key, depth=0):
        print 'computing results for ' + key
        r_search = self.s_eng.search(key)
        for keyword in r_search:
            try:
                self.session.query(InstantKeyword).filter(InstantKeyword.keyword == keyword).one()
            except NoResultFound, e:
                key_entry= InstantKeyword(keyword, depth, r_search.index(keyword))
                self.session.add(key_entry)
                self.keywords.append(key_entry)
        self.session.commit()
        
    def simpleSearch(self):
        i = 0
        while(True):
            try:
                key = self.dictionary.next()
            except self.Error:
                print 'finished'
                '''
                i = 1
                keywords2 = keywords.copy()
                for key in keywords2:
                    r_search = self.s_eng.search(key)
                '''
                break
            self.__search_and_add_keywords_to_database(key, i)
            
                
            
#to create the schema            
#Base.metadata.create_all(engine)


#a = InstantKeyword('test', 1, 2)
#session.add(a)
#session.commit()
#print session.query(InstantKeyword).all()

#class KeywordManagerTest(unittest.TestCase, KeywordManager):
    

if __name__ == '__main__':
    unittest.main()
        
    
    