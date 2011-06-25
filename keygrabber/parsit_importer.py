from lxml import etree
import pymongo

connection = pymongo.Connection()
db = connection.webkeywords

tree = etree.parse("result_title_list.xml")

for element in tree.iter('document'):
	index = int(element.attrib.get('index'))
	keyword = element.getchildren()[0].text
	category = element.getchildren()[1].getchildren()[0].text
	mongok = db.orderedkeys.find_one(dict(index=index, keyword=keyword))
	mongok['category'] = category
	db.orderedkeys.save(mongok)

print 'categories added to db'
print 'removing %i keys' % db.orderedkeys.find( { 'category' : { '$exists' : False } } ).count()

for mongok in db.orderedkeys.find( { 'category' : { '$exists' : False } } ):
	db.orderedkeys.remove(mongok)
	
print 'end'
	
