# -*- coding: UTF-8 -*-
from adwords import keyword_adwords as kad
import pymongo
import logging


log = logging.getLogger('ordering')
log.addHandler(logging.FileHandler('/tmp/keygrabber-ordering.log', 'w'))

connection = pymongo.Connection()
DB = connection.webkeywords
CL_IN = DB.crawlerCopy
CL_OUT = DB.orderedkeys

def create_ordered_collection(inst_list):
	'''
	Create the CL_OUT collection adding an index element
	'''
	#add index
	log.info('adding index')
	for i, key in enumerate(inst_list):
		key['index']=i 
	#save to orderedkeys collection
	CL_OUT.drop()
	log.info('adding ordered keys :'+str(len(inst_list)))
	a = CL_OUT.insert(inst_list)
	CL_OUT.ensure_index('index')
	CL_OUT.ensure_index('parent')
	log.info('collection created successfully')
	return inst_list

def retrieve_data_from_db(limit=0):
	keys = list()
	for item in CL_IN.find().limit(limit):
		keys.append(item)
	return keys
	
def get_adwords_data(keys):	
	'''
	Get adwords data and save it
	'''
	for item in keys:
		d = kad.get_keyword_info(item.get('keyword'))
		item['global_searches'] = d.get('global_searches')
		item['regional_searches'] = d.get('regional_searches')
		CL_IN.save(item)
	return keys
	
def order_by_adwords_data(keys):
	keys.sort(key=lambda x: int(x.get('global_searches')) if x.get('global_searches') is not None else 0, reverse=True)
	for key in keys:
		for k in keys:
			if key.get('keyword').startswith(k.get('keyword')+' ') and k.get('global_searches', 0) >= key.get('global_searches', 0):
				print 'parent of', key.get('keyword'), ' is ', k.get('keyword')
				key['has_child'] = True
				break
	return keys

def adwords_ordering(limit = 0):
	'''
	Il nuovo algoritmo di
	ordinamento funziona così: si fa query a Google per ogni keyword per
	recuperare traffico e CPC. Si crea un index ordinando i titoli da
	quelli che fanno più traffico a quelli che fanno meno traffico usando
	il traffico globale. I figli sono dati dai titoli che iniziano col
	titolo padre se i titoli figli fanno meno traffico del titolo padre
	(es: come scaricare musica è figlio di come scaricare se, ad esempio,
	come scaricare musica fa 100 ricerche al mese e come scaricare ne fa
	10000)
	
	I figli sono dati dai titoli che iniziano col
	titolo padre se i titoli figli fanno meno traffico del titolo padre
	sia legata ad adwords 02:06:20 PM
	se i due titoli hanno traffico 02:06:27 PM
	0 ? 02:06:29 PM
	 
	Salvatore Aranzulla 02:06:35 PM
	beh fai <=
	e chi si è visto si è visto
	'''
	keys = retrieve_data_from_db(limit)
	#keys = get_adwords_data(keys)
	ordered_keys = order_by_adwords_data(keys)
	create_ordered_collection(ordered_keys)
		
def fast_order(self):
	'''
	Algorithm which creates index ffor the keywords based on the values got from the crawler
	'''
	log.warning('Start fast ordering')
	
	inst_list = list()
	cursors = list()
	wrong_list = list()
	
	def _update_threshold(dicts= 100, level = 7, depth =4, dbplace=10):	
		m_dicts = 1
		m_level = 0
		m_depth = 0
		m_dbplace = 1
		
		yield (m_dicts, m_level, m_depth, m_dbplace)
		
		while m_dicts < dicts:
			m_dbplace = m_dbplace + 1
			if m_dbplace > dbplace:
				m_depth = m_depth +1
				m_dbplace = 1
			if m_depth > depth:
				m_level = m_level + 1
				m_depth = 0
				m_dbplace = 0
			if m_level > level:
				m_dicts = m_dicts +1
				m_level = 0
				m_depth = 0
				m_dbplace = 0
			yield (m_dicts, m_level, m_depth, m_dbplace)
	
	root = CL_IN.find_one(dict(dicts=0, parent=None))
	max_dicts = CL_IN.find().sort([('dicts',pymongo.DESCENDING),])[0].get('dicts')
	max_level = CL_IN.find().sort([('level',pymongo.DESCENDING),])[0].get('level')
	max_depth = CL_IN.find().sort([('depth',pymongo.DESCENDING),])[0].get('depth')
	max_dbplace = CL_IN.find().sort([('dbplace',pymongo.DESCENDING),])[0].get('dbplace')

	for (dicts, level, depth, dbplace) in _update_threshold(max_dicts, max_level, max_depth, max_dbplace):
		log.info("threashold:"+str(dicts)+" "+str(level)+" "+str(depth)+" "+str(dbplace))
		for letter in ascii_lowercase:
			items = [item for item in CL_IN.find(dict(keyword=re.compile('^'+root.get('keyword')+' '+letter), dicts=dicts, level=level, depth=depth, dbplace=dbplace))]
			if len(items) > 0:
				inst_list.extend(items)
		log.info("successfully ordered :"+str(len(inst_list)))
	return inst_list

def do_fast_order():
	ordered_keys = fast_order()
	create_ordered_collection(ordered_keys)
	
if __name__ == "__main__":
	adwords_ordering(10000)
