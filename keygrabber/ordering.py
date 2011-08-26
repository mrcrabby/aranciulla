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
			if key.get('keyword').startswith(k.get('keyword')) and k.get('global_searches', 0) >= key.get('global_searches', 0) 
				print 'parent of', key.get('keyword'), ' is ', k.get('keyword')
				key['parent'] = k.get('keyword')
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
	keys = get_adwords_data(keys)
	ordered_keys = order_by_adwords_data(keys)
	create_ordered_collection(ordered_keys)
		

if __name__ == "__main__":
	adwords_ordering(10000)
