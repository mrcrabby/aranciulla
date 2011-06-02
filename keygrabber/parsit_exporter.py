from lxml import etree
import pymongo

connection = pymongo.Connection()
db = connection.webkeywords

root = etree.Element('documents')
for item in db.orderedkeys.find():
	document = etree.SubElement(root,'document', index=str(item.get('index')))
	text = etree.SubElement(document,'text')
	text.text = item.get('keyword')

print(etree.tostring(root, pretty_print=True))


"""
<document index="1"><text>come arredare casa</text></document>
"""
