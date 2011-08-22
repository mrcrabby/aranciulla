import os
import sys
sys.path.append('.')
import pymongo
import adwords.keyword_adwords as kad


connection = pymongo.Connection()
db = connection.webkeywords

for item in db.orderedkeysCopy.find():
	d = kad.get_keyword_info(item.get('keyword'))
	item['global_searches'] = d.get('global_searches')
	item['regional_searches'] = d.get('regional_searches')
	print item
	db.save(item)
