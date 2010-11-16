import sys
import getopt
import math

#python getopt.py list 10 list2 20 

class DownloadEntry():
    def __init__(self, title, score=0):
        self.title = title
        self.score = score
    
    def append_score(self, score):
        self.score += score
    
    def str(self, compact):
        if compact:
            return self.title
        return self.__str__()
        
    def __str__(self):
        return 'title:%s score:%d' % (self.title, self.score)
    
    def __repr__(self):
        return self.__str__()

def usage():
    print('''
Genlist - List generator

Usage: python genlist.py [file] [visits]

Options:
    -h --help: show this help message
    -o filename --output filename: write result to file
    -c --compact: show compact results
    -d num --diverge-factor num: diversion factor
    ''')
   
def main():
    opts, extraparams = getopt.gnu_getopt(sys.argv[1:], "ho:vcd:", ["help", "output=", "compact", "diverge-factor="])
    
    verbose = False
    output = None
    compact = False
    pow = 1
    
    for o, a in opts:
        if o == "-v":
            verbose = True
        elif o in ("-h", "--help"):
            usage()
            sys.exit()
        elif o in ("-o", "--output"):
            output = a
        elif o in ("-c", "--compact"):
            compact = True
        elif o in ("-d", "--diverge-factor"):
            pow = int(a)
        else:
            assert False, "unhandled option"
            
    files = dict()
    for i in range(len(extraparams)):
        if i % 2 :
            files[extraparams[i-1]] = extraparams[i]
    #start the main algorithm
    d = {}
    l = [] 
    for (filename, filescore) in files.iteritems():
        filescore = int(filescore)/10.00
        f = open(filename, 'r')
        content = f.readlines()
        f.close()
        n_entries = len(content)
        for i, line in zip(range(len(content)), content):
            #check if line is in final dict:
            #    if yes -> increment score
            #    if not -> add it to the dict
            if line in d:
                d[line].append_score(math.pow(n_entries/100.00, pow)*filescore)
            else:
                d[line] = DownloadEntry(line[:-1], math.pow(n_entries/100.00, pow)*filescore)
            n_entries -= 1
    #create the output list
    for key, value in d.iteritems():
        l.append(value)
    l.sort(key=lambda x: x.score, reverse=True)
    if output:
        f = open(output, 'w')
        f.writelines([obj.str(compact)+'\n' for obj in l])
        f.close()
    else:
        print([obj.str(compact)+'\n' for obj in l])
        

if __name__ == "__main__":
    main()
