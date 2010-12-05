#!/usr/bin/python
# -*- coding: UTF-8 -*-

import json
from urllib import urlencode
import urllib2
import re
import HTMLParser
import os

from aralib.adwordsApi.aw_api.Client import Client
client = Client(path='../aralib/adwordsApi')
targeting_idea_service = client.GetTargetingIdeaService('https://adwords.google.com', 'v201003')

class Google():
    def __init__(self):
        self.html_parser = HTMLParser.HTMLParser()
            
    def getKeywords(self, keyword, *args, **kwargs):
        
        def __get_g_json(term): 
            data = urllib2.urlopen('http://clients1.google.it/complete/search?'+urlencode({'q':(term+u' ').encode('utf-8'), 'hl':'it', 'client':'hp'})).read()
            HTMLtag = re.compile('<\/*b>')      # Matches HTML tags
            data = unicode(data, 'iso-8859-15')
            g_list = json.loads(data[19:-1])
            return [self.html_parser.unescape(HTMLtag.sub('', entry[0])) for entry in g_list[1]]
        
        keywords = list()
        g_json=__get_g_json(unicode(keyword, 'utf-8'))
        for entry in g_json:
            keywords.append(entry)
        add_keywords = list()
        for keyword in keywords:
            g_json = __get_g_json(keyword)
            for entry in g_json[1:3]:
                add_keywords.append(entry)
        keywords.extend(add_keywords)
        return keywords
    
    def __adwords_parse(self, page):
        keywords = list()
        if 'entries' in page:
            for result in page.get('entries'):
                data = result.get('data')
                for single_data in data:
                    for (k,v) in single_data.iteritems():
                        if k == 'value':
                            value = v
                        if k == 'key':
                            key = v
                            if key == 'KEYWORD':
                                keyword = value.get('value').get('text')
                                match_type = value.get('value').get('matchType')
                            elif key == 'GLOBAL_MONTHLY_SEARCHES':
                                global_score = int(value.get('value','0'))
                            elif key == 'AVERAGE_TARGETED_MONTHLY_SEARCHES':
                                regional_score = int(value.get('value','0'))
                                if global_score != 0:
                                    keywords.append(dict(keyword=keyword, match_type=match_type, global_score=global_score, regional_score=regional_score))
        return keywords
    
    def getAdwordsKeywords(self, keyword, mode='BROAD'):
        keyword_entries = list()
        selector = {
            'searchParameters': [{
                'type': 'RelatedToKeywordSearchParameter',
                'keywords': [{
                    'text': keyword,
                    'matchType': mode
                }]
            },{
               'type': 'IdeaTextMatchesSearchParameter',
               'included': [keyword]
            },{
               'type': 'KeywordMatchTypeSearchParameter',
               'keywordMatchTypes': [mode]
            },{
               'type': 'LanguageTargetSearchParameter',
               'languageTargets': [{'languageCode':'it'}]
            },{
               'type': 'CountryTargetSearchParameter',
               'countryTargets': [{'countryCode':'IT'}]
            }],
            'ideaType': 'KEYWORD',
            'requestType': 'IDEAS',
            'requestedAttributeTypes': ['KEYWORD','GLOBAL_MONTHLY_SEARCHES', 'AVERAGE_TARGETED_MONTHLY_SEARCHES'],
            'paging': {
                'startIndex': '0',
                'numberResults': '1000'
            }
        }
        
        #execute until no exceptions
        for i in range(30):
            try:
                page = targeting_idea_service.Get(selector)[0]
            except:
                continue
            else:
                break
            
        keyword_entries += self.__adwords_parse(page)
    
        return keyword_entries
        
