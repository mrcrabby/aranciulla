import os
import sys
sys.path.append('.')
import pymongo
import adwords.keyword_adwords as kad


connection = pymongo.Connection()
db = connection.webkeywords
cl = db.orderedkeysCopy

def get_adwords_data_and_save():
	for item in db.orderedkeysCopy.find():
		d = kad.get_keyword_info(item.get('keyword'))
		item['global_searches'] = d.get('global_searches')
		item['regional_searches'] = d.get('regional_searches')
		db.orderedkeysCopy.save(item)

def create_csv():
	print 'keyword, index, global, regional'
	for item in cl.find():
		print '%s,%s,%s,%s' % (item.get('keyword'), item.get('index'), item.get('global_searches'), item.get('regional_searches'))


if __name__ == '__main__':
	create_csv()
