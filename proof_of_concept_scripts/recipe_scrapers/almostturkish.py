# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 20:38:02 2015

@author: bethanygarcia
Start for almostturkish.blogspot.com
"""

from urllib2 import urlopen
from bs4 import BeautifulSoup, NavigableString, Tag
import nltk, re, pprint
from nltk import word_tokenize
from nltk import TreebankWordTokenizer

html = urlopen("http://almostturkish.blogspot.com/2010/02/collard-greens-soup-karalahana-corbas.html") 
bsObj = BeautifulSoup(html, 'html5lib')

recipe_title = bsObj.find("h3", {"class":"post-title entry-title"}).getText().strip()
recipe = bsObj.find("div", {"class":"post-body entry-content"})
recipe_list = [s for s in recipe.descendants if isinstance(s, NavigableString)]
recipe_photo = recipe.img.attrs['src']
recipe_text = []

for child in recipe_list:
    word_list = ['js', 'script', 'function', 'Pin It', 'Tweet']
    if child.string:        
        #http://stackoverflow.com/questions/3271478/check-list-of-words-in-another-string        
        if any(word in child.string for word in word_list):
            continue 
        elif u'\n' == child.string:
            continue
        elif child.string not in recipe_text:
            recipe_text.append(child.string)
            
sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
recipe_text = '\n'.join(recipe_text)
parse_test = sent_detector.tokenize(recipe_text)


print recipe_list
print '\n'
print '\n'
print recipe_text
print '\n'
print parse_test

#for item in test_list:
#    print item + u'\n'

#print recipie
#print '\n\n\n'
#for i in remove_span:
#    print i
#[s.extract() for s in recipie('a')]
#re.compile(r'<img.*?/>')
#if isinstance(s, NavigableString)
#[s for s in bsObj.find("div", {"itemprop":"articleBody"})]
#http://almostturkish.blogspot.com/2006/12/turkish-feta-potato-rolls-frnda-sigara.html
#http://almostturkish.blogspot.com/2010/02/collard-greens-soup-karalahana-corbas.html
#http://almostturkish.blogspot.com/2009/07/stuffed-zucchinis-with-ground-meat-etli.html


    
