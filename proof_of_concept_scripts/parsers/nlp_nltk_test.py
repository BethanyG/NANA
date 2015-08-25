# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 23:38:13 2015

@author: bethanygarcia
"""
#import json
# from jsonrpc import ServerProxy, JsonRpc20, TransportTcpIp
#import jsonrpclib
import os
from nltk.parse import stanford
from nltk.corpus import treebank
from nltk.corpus import wordnet as wn
from nltk.tree import *

os.environ['STANFORD_PARSER'] = 'stanford_jars/stanford-parser.jar'
os.environ['STANFORD_MODELS'] = 'stanford_jars/stanford-parser-3.5.2-models.jar'

parser = stanford.StanfordParser(model_path='/Users/bethanygarcia/.virtualenvs/Flask_project/stanford_jars/edu/stanford/nlp/models/lexparser/englishPCFG.ser.gz')
sentence = parser.raw_parse(("1/8 teaspoon asafetida (hing)"))


#for s in sentence.subtrees(lambda t: t.height() ==3):
#    print(s)
#def filt(s):
#    return s.label() == 'NP'

for myListiterator in sentence:
    #for subtree in myListiterator.subtrees(filter = filt):
    #    print subtree
    #for s in myListiterator.subtrees(lambda t: t.height() ==3):
        #s.subtrees(filter = lambda st: st.label() == 'NP')
    #    s.subtrees(filter = filt)
    for s in myListiterator.subtrees(filter = lambda st: st.label() == 'NP' or st.label() == 'QP'):
        s = s.flatten()
        st = s.leaves()
        print st



'''for myListiterator in sentence:
    print type(myListiterator)
    for t in myListiterator:
        print type(t)
        for s in myListiterator:
            print s
            print type(s)            
            #new_tree = Tree.fromstring(s)'''

#new_sentence = [sentence(i)[0] for i in sentence]
#print '\n\n'
#print new_sentence

#bracketed_parse = " ".join( [i.strip() for i in sentence if i.strip()[0] == "("] )
#print bracketed_parse





'''print(type(result))
#pprint(result)
print('\n')
print('\n')
pprint(result)'''