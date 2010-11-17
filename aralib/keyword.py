#!/usr/bin/python
# -*- coding: UTF-8 -*-


from xml.dom.minidom import parseString
from progressbar import ProgressBar
from xml.dom.minidom import Document
import urllib2


stopwords = (u'ad', u'al', u'allo', u'ai', u'agli', u'all', u'agl', u'alla', u'alle', u'con', u'col', u'coi', u'da', u'dal', u'dallo', u'dai', u'dagli', u'dall', u'dagl', u'dalla', u'dalle', u'di', u'del', u'dello', u'dei', u'degli', u'dell', u'degl', u'della', u'delle', u'in', u'nel', u'nello', u'nei', u'negli', u'nell', u'negl', u'nella', u'nelle', u'su', u'sul', u'sullo', u'sui', u'sugli', u'sull', u'sugl', u'sulla', u'sulle', u'per', u'tra', u'contro', u'io', u'tu', u'lui', u'lei', u'noi', u'voi', u'loro', u'mio', u'mia', u'miei', u'mie', u'tuo', u'tua', u'tuoi', u'tue', u'suo', u'sua', u'suoi', u'sue', u'nostro', u'nostra', u'nostri', u'nostre', u'vostro', u'vostra', u'vostri', u'vostre', u'mi', u'ti', u'ci', u'vi', u'lo', u'la', u'li', u'le', u'gli', u'ne', u'il', u'un', u'uno', u'una', u'ma', u'ed', u'se', u'perché', u'anche', u'come', u'dov', u'dove', u'che', u'chi', u'cui', u'non', u'più', u'quale', u'quanto', u'quanti', u'quanta', u'quante', u'quello', u'quelli', u'quella', u'quelle', u'questo', u'questi', u'questa', u'queste', u'si', u'tutto', u'tutti', u'a', u'c', u'e', u'i', u'l', u'o', u'ho', u'hai', u'ha', u'abbiamo', u'avete', u'hanno', u'abbia', u'abbiate', u'abbiano', u'avrò', u'avrai', u'avrà', u'avremo', u'avrete', u'avranno', u'avrei', u'avresti', u'avrebbe', u'avremmo', u'avreste', u'avrebbero', u'avevo', u'avevi', u'aveva', u'avevamo', u'avevate', u'avevano', u'ebbi', u'avesti', u'ebbe', u'avemmo', u'aveste', u'ebbero', u'avessi', u'avesse', u'avessimo', u'avessero', u'avendo', u'avuto', u'avuta', u'avuti', u'avute', u'sono', u'sei', u'è', u'siamo', u'siete', u'sia', u'siate', u'siano', u'sarò', u'sarai', u'sarà', u'saremo', u'sarete', u'saranno', u'sarei', u'saresti', u'sarebbe', u'saremmo', u'sareste', u'sarebbero', u'ero', u'eri', u'era', u'eravamo', u'eravate', u'erano', u'fui', u'fosti', u'fu', u'fummo', u'foste', u'furono', u'fossi', u'fosse', u'fossimo', u'fossero', u'essendo', u'faccio', u'fai', u'facciamo', u'fanno', u'faccia', u'facciate', u'facciano', u'farò', u'farai', u'farà', u'faremo', u'farete', u'faranno', u'farei', u'faresti', u'farebbe', u'faremmo', u'fareste', u'farebbero', u'facevo', u'facevi', u'faceva', u'facevamo', u'facevate', u'facevano', u'feci', u'facesti', u'fece', u'facemmo', u'faceste', u'fecero', u'facessi', u'facesse', u'facessimo', u'facessero', u'facendo', u'sto', u'stai', u'sta', u'stiamo', u'stanno', u'stia', u'stiate', u'stiano', u'starò', u'starai', u'starà', u'staremo', u'starete', u'staranno', u'starei', u'staresti', u'starebbe', u'staremmo', u'stareste', u'starebbero', u'stavo', u'stavi', u'stava', u'stavamo', u'stavate', u'stavano', u'stetti', u'stesti', u'stette', u'stemmo', u'steste', u'stettero', u'stessi', u'stesse', u'stessimo', u'stessero', u'stando', u'far', u'piu', u'click', u'collegati', u'sito', u'Internet', u'file', u'pulsante', u'voce', u'finestra', u'avanti', u'fine', u'infine', u'apre', u'a questo punto', u'poi', u'barra', u'devi', u'puoi', u'avere', u'vuoi', u'se', u'fare', u'subito', u'clicca', u'pagina', u'uno', u'due', u'tre', u'dopo', u'essere', u'possono', u'tasto', u'mouse', u'destro', u'sinistro', u'appena', u'sempre', u'destra', u'sinistra', u'modulo', u'tutte', u'tutti', u'quindi', u'accanto', u'sotto', u'presente', u'collocato', u'collocata', u'ormai', u'molto', u'poco', u'for', u'in', u'per', u'is')

bannedwords = set([u'ke', u'keygen', u'yhaoo', u'dounload', u'downlo', u'gartis', u'ome', u'adesso', u'grazie', u'ecco', u'forum', u'italino', u'licenza', u'descargar', u'gratuit', u'telecharger', u'7F5', u'win32', u'win 32', u'descargare', u'grati', u'trojandownloader', u'fastwebnet', u'scn', u'sondrio', u'mese', u'ilpc', u'vers', u'istalare', u'downloada', u'scansini', u'gratisyahoo', u'yahoo', u'answers', u'2004', u'0F49', u'warcraft', u'9F5', u'47Fc', u'9F5', u'cme', u'euro', u'crack', u'free', u'ita', u'seriale', u'donwoland', u'dowloand', u'cazzo', u'yahoo', u'answers', u'dowland', u'xke', u'nn', u'descarca', u'dawnload', u'2009', u'2010', u'2008', u'2007', u'scaricre', u'gradis', u'dowload', u'wnload', u'telecharge', u'donwload', u'itliano', u'gigi', u'porno', u'saks fifth ave link', u'prer', u'downloades', u'downloads', u'3F15', u'3F14', u'xnavigation', u'tuttogratis', u'tutto gratis', u'softonic', u'aranzulla', u'serial', u'full', u'inglis', u'scarecari', u'gratias', u'downloadf', u'dawload', u'architettura', u'arch', u'windw', u'serverfr', u'kadu', u'poret', u'migliorr', u'x', u'gta', u'sever', u'1F7F7', u'malavida', u'8F5', u'vogli', u'alpha', u'beta', u'porn', u'porno', u'sex', u'sexy', u'sesso', u'gay', u'lesbo', u'sotwer', u'donwold', u'softwere', u'pi', u'messanger', u'ultimaa', u'scaricanuova'])

bannedchars = set([u'.', u',', u'\'', u'"'])

class KeywordEntry():
    def __init__(self, keyword, key):
        self.keyword = unicode(keyword)
        self.key = unicode(key)
        self.children = list()
        self.selected = False
            
    def __str__(self):
        return 'keyword:%s key:%s' % (self.keyword, self.key)
    
    def __repr__(self):
        return self.__str__()

class Tree():
    def __init__(self, main):
        self.el = main
        self.next = list()
        
        
def relation(key1, key2):
    if key1 != key2:
        return all(word in key2.split() for word in key1.split())
    else:
        return False




def __retrieve_keyword_presence_in_page(url, keyword, filter_done, filter_missed, *args, **kwargs):
    if any(word in filter_missed for word in keyword.split()):
        return False
    
    res = True
    
    words = [word for word in keyword.split() if word not in filter_done.union(filter_missed)]
    for word in words:
        try:
            page = urllib2.urlopen(url+word).read()
        except UnicodeEncodeError:
            #pdb.set_trace()
            continue
        if "Nessun articolo trovato. Vuoi provare una ricerca diversa?" in page:
            filter_missed.add(word)
            res = False
        else:
            filter_done.add(word)
    
    return res

        
def __gen_xml(keyword, keywords, lower_bound, upper_bound, url=None,  *args, **kwargs):        
    
    filter_done = set()
    filter_missed = set()
    
    filter = False
    if url:
        filter = True
    valid = True
    
    doc = Document()
    cat = doc.createElement("parent")
    cat.setAttribute('key', keyword)
    doc.appendChild(cat)
    
    pbar = ProgressBar(maxval=len(keywords)).start()
    trees = list()        
    for i,obj in enumerate(keywords):
        pbar.update(i)
        if len(obj.children) > lower_bound:
            tree = None
            if filter:
                if __retrieve_keyword_presence_in_page(url, obj.key, filter_done, filter_missed):
                    valid = True
                else:
                    valid = False
             
            if valid:
                tree = Tree(obj.keyword)
            
            j = 0
            for entry in obj.children:
                if filter:
                    if __retrieve_keyword_presence_in_page(url, entry.key, filter_done, filter_missed):
                        valid = True
                        j += 1
                    else:
                        valid = False
                
                if valid:
                    tree.next.append(unicode(entry.keyword))
                
                if j >= upper_bound:
                    break
            if tree:
                trees.append(tree)
    
    #Create the xml now
    for tree in trees:
        if len(tree.next) > lower_bound:
            child = doc.createElement("child")
            child.setAttribute("key", tree.el)
            cat.appendChild(child)
            for el in tree.next:
                nephew = doc.createElement('nephew')
                nephew.setAttribute('key', el)
                child.appendChild(nephew)
    
    pbar.finish()
    sys.stdout.write('\n')
    return doc
    
def filter_bannedwords(content):
    return [keyword for keyword in content if all(word not in bannedwords for word in keyword.split())]

def filter_bannedchars(keywords):
    return [keyword for keyword in keywords if all(char not in keyword for char in bannedchars)]

def genKey(keyword, generated_keyword):
    '''Per identificarle, basta eliminare le stopword e riordinare le parole delle keyword in modo tale da individuare quelle duplicate, che vanno rimosse.'''
    generated_keyword = unicode(generated_keyword)
    keyword = unicode(keyword)
    
    list = generated_keyword.split()
    
    #put keyword at top
    while True: 
        if keyword in list:
            list.pop(list.index(keyword))
        else:
            break
    
    #remove stopwords    
    for stopword in stopwords:
        if stopword in list:
            list.pop(list.index(stopword))
    
    list.sort()
    
    return ' '.join([keyword]+list)
