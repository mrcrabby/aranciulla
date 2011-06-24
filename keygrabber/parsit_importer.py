from lxml import etree
import pymongo
import ipdb

connection = pymongo.Connection()
db = connection.webkeywords

tree = etree.parse("result_title_list.xml")

for element in tree.iter('document'):
	index = element.attrib.get('index')
	keyword = element.getchildren()[0].text
	categoria = element.getchildren()[1].getchildren()[0].text
	print '%s %s %s' % (index, keyword, categoria)
	print db.orderedkeys.find_one(dict(keyword=keyword, index=index))
