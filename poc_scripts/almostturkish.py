# -*- coding: utf-8 -*-
"""
Created on Sun Aug  9 20:38:02 2015

@author: bethanygarcia
Start for almostturkish.blogspot.com
"""

from urllib2 import urlopen
from bs4 import BeautifulSoup, NavigableString, Tag
import re

html = urlopen("http://almostturkish.blogspot.com/2006/12/turkish-feta-potato-rolls-frnda-sigara.html") 
bsObj = BeautifulSoup(html, 'html5lib')

recipie_title = bsObj.find("h3", {"class":"name"}).getText().strip()
recipie = bsObj.find("div", {"class":"post-body entry-content"})
#recipie_list = recipie.
recipie_photo = recipie.img.attrs['src']
test_list = []

#for child in recipie_list:
#    word_list = ['js', 'script', 'function', 'Pin It', 'Tweet']
#    if child.string:        
        #http://stackoverflow.com/questions/3271478/check-list-of-words-in-another-string        
#        if any(word in child.string for word in word_list):
#            continue 
#        elif u'\n' == child.string:
#            continue
#        elif child.string not in test_list:
#            test_list.append(child.string)

#recipie_list = [s.strip() for s in recipie.descendants if isinstance(s, NavigableString)]

#print recipie_title
#print recipie_photo
print recipie_list


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


    
