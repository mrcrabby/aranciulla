import pymongo

connection = pymongo.Connection()
db = connection.webkeywords

print "keyword, index, discarded"

for item in db.orderedkeys.find():
	keyword = item.get('keyword')
	words = keyword.split()
	if len(words) > 1:
		word = words[1]
		if word.endswith('are') or word.endswith('ere') or word.endswith('ire'):
			print "%s, %s" % (item.get('keyword'), item.get('index')) 
		else:
			print "%s, %s, True" % (item.get('keyword'), item.get('index')) 
