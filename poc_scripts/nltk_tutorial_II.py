# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 12:29:59 2015

@author: bethanygarcia
"""
from __future__ import print_function, division
import nltk, re, pprint
from nltk import word_tokenize
from urllib2 import urlopen
#from nltk.corpus import gutenberg
#from nltk.corpus import webtext
#from nltk.corpus import nps_chat
#from nltk.corpus import brown
#from nltk.corpus import udhr
#from nltk.corpus import stopwords
#from nltk.corpus import swadesh
#from nltk.corpus import wordnet as wn

url = 'http://www.gutenberg.org/files/2554/2554.txt'
response = urlopen(url)
raw= response.read()#.encode('ascii')

tokens = word_tokenize(raw)
text = nltk.Text(tokens)



#print (type(text))
#print (text[1024:1062])
#print (text.collocations())

#print (type(raw))
#print (len(raw))
#print (raw[:75])








#motorcar = wn.synset('car.n.01')
#types_of_motorcar = motorcar.hyponyms()
#print (types_of_motorcar[0])

#print(sorted(lemma.name() for synset in types_of_motorcar for lemma in synset.lemmas()))


#print (wn.synsets('tablespoon'))
#print (wn.synsets('onion'))
#print (wn.synset('onion.n.01').lemma_names())

#print (wn.synsets('tablespoon'))
#print (wn.synset('tablespoon.n.01').lemma_names())

#fr2en = swadesh.entries(['fr','en'])
#print (fr2en)


#print (swadesh.fileids())



#puzzle_letters = nltk.FreqDist('egivrvonl')
#obligatory = 'r'
#wordlist = nltk.corpus.words.words()
#print ([w for w in wordlist if len(w) >= 6 and obligatory in w and nltk.FreqDist(w) <= puzzle_letters])


#print (stopwords.words('english'))

#def content_fraction(text):
#    stopwords = nltk.corpus.stopwords.words('english')
#    content = [w for w in text if w.lower() not in stopwords]
#    return float(len(content)) / len(text)

#print (content_fraction(nltk.corpus.reuters.words()))

#def unusual_words(text):
#    text_vocab = set(w.lower() for w in text if w.isalpha())
#    english_vocab = set(w.lower() for w in nltk.corpus.words.words())
#    unusual = text_vocab - english_vocab
#    return sorted(unusual)

#print (unusual_words(nltk.corpus.gutenberg.words('austen-sense.txt')))
#print (unusual_words(nltk.corpus.nps_chat.words()))
#languages = ['Chickasaw', 'English', 'German_Deutsch','Greenlandic_Inuktikut', 'Hungarian_Magyar', 'Ibibio_Efik']
#cfd = nltk.ConditionalFreqDist((lang, len(word)) for lang in languages for word in udhr.words(lang + '-Latin1'))
#print(cfd.plot(cumulative=True))



#cfd = nltk.ConditionalFreqDist((genre, word)for genre in brown.categories()for word in brown.words(categories=genre))
#genres = ['news', 'religion', 'hobbies', 'science_fiction', 'romance', 'humor']
#modals = ['can', 'could', 'may', 'might', 'must', 'will']
#print (cfd.tabulate(conditions=genres, samples=modals))




#news_text = brown.words(categories='news')
#fdist = nltk.FreqDist(w.lower() for w in news_text)
#modals = ['when', 'what', 'why', 'where', 'who']
#for m in modals:
#        print(m+ ':', fdist[m], end=' ')


#print (brown.categories())
#print (brown.words(categories='news'))
#print (brown.words(fileids=['cg22']))
#print (brown.sents(categories=['news', 'editorial', 'reviews']))
#chatroom = nps_chat.posts('10-19-20s_706posts.xml')
#print (chatroom[123])


#for fileid in webtext.fileids():
#    print(fileid, webtext.raw(fileid)[:65], "...")

'''for fileid in gutenberg.fileids():
    num_chars = len(gutenberg.raw(fileid))
    num_words = len(gutenberg.words(fileid))
    num_sents = len(gutenberg.sents(fileid))
    num_vocab = len(set(w.lower() for w in gutenberg.words(fileid)))
    print(round(num_chars/num_words), round(num_words/num_sents), round(num_words/num_vocab), fileid)'''