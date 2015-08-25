# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 11:21:59 2015

@author: bethanygarcia
"""

from textblob import TextBlob
from textblob.np_extractors import ConllExtractor
from textblob.taggers import NLTKTagger

extractor = ConllExtractor()




blob =  TextBlob('carrots peeled and sliced in small pieces')
#print blob.tags
print blob.noun_phrases
#print blob.words
print '\n\n'
print blob.ngrams(n=2)
print '\n\n'
#print blob.pos_tags

#for s in sentence.subtrees(lambda t: t.height() ==3):
#    print(s)
