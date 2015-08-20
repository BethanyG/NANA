# -*- coding: utf-8 -*-
"""
Created on Mon Aug 17 13:16:54 2015

@author: bethanygarcia

self.sourceurl = None
        self.photo = None        
        self.title = None
        self.description = None
        self.preptime =  None
        self.cooktime = None
        '''eventually, this will contain an ingredient object,
           populated by the parsers and the nutrient anayalizer class'''
        self.ingredients = None 
        self.directions = None
        self.servings = None



"""

from __future__ import print_function, division
from urllib2 import urlopen
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
#import nltk, re, pprint
#from nltk import word_tokenize
#from nltk import TreebankWordTokenizer

html = urlopen("http://www.gourmet.com/recipes/2000s/2006/12/pizza-with-fontina-proscuitto-and-arugula.html") 
bsObj = BeautifulSoup(html, 'html5lib')

recipe = bsObj.find("div", {"class":"recipe"})

if bsObj.find("h1", {"class":"header"}).getText():
    title = bsObj.find("h1", {"class":"header"}).string
if bsObj.find("div", {"class":"text"}):
    title = bsObj.find("div", {"class":"text"}).string


photo = bsObj.find("div", {"class":"w"}).img.attrs['src']

if bsObj.find("div", {"class":"introduction"}):
    description = bsObj.find("div", {"class":"introduction"}).string
if bsObj.find("div", {"class":"text"}):
    description = [''.join(item.getText().split('<em>')) for item in bsObj.find("div", {"class":"text"}).contents]
    description = description[0]

ingreds_list = [''.join(item.getText().split('\n')) for item in bsObj.findAll("div", {"class":"ingredient-set"})]
ingredients = [item.strip() for item in ingreds_list]
directions = ''.join(bsObj.find("div", {"class":"preparation"}).getText().split('\n'))
servings_I = bsObj.find("div", {"class":"yeild"})
#servings_II = servings_I.find("span", {"class":"label"})



print('\n')
print(title)
print('\n')
print(photo)
print('\n')
print(ingredients)
print('\n')
print(directions)
print('\n')
print('\n')
print(description)


#http://www.gourmet.com/recipes/2000s/2009/01/spaghetti-and-meatballs.html
#http://www.gourmet.com/recipes/2000s/2008/07/beeftenderloin.html