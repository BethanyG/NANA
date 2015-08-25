# -*- coding: utf-8 -*-
"""
Created on Mon Aug 10 00:52:00 2015

@author: bethanygarcia
"""
from __future__ import print_function, division
from urllib2 import urlopen
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import nltk, re, pprint
#from nltk import word_tokenize
#from nltk import TreebankWordTokenizer

html = urlopen("http://www.101cookbooks.com/archives/cocagne-bean-artichoke-salad-recipe.html") 
bsObj = BeautifulSoup(html, 'html5lib')

filter_list = [u'\n\n', u'\n\n\n', u'\n', " '", ' === end recipe div === ']
recipie = bsObj.find("div", {"id":"recipe"})
recipie_title = recipie.h1.getText().strip()

if recipie.p.i:    
    recipie_descript = recipie.p.i.getText().strip()

if recipie.find("span", {"class":"preptime"}):
    recipie_prep = recipie.find("span", {"class":"preptime"}).getText().strip()

if recipie.find("span", {"class":"cooktime"}):
    recipie_cook = recipie.find("span", {"class":"preptime"}).getText().strip()


recipie_ingreds = [item.getText().strip() for item in recipie.blockquote.findAll('p') if item not in filter_list]
recipie_ingreds = "\n".join(recipie_ingreds)
recipie_ingreds = filter(None, recipie_ingreds)
recipie_ingreds = recipie_ingreds.split('\n')

recipie_directions = [item.string for item in recipie.blockquote.next_siblings if item not in filter_list]
recipie_directions = filter(None, recipie_directions)

for item in recipie_directions:
    if "Serves" in item:
        recipie_servings = item.string
        recipie_directions.remove(item)
    else: continue

recipie_directions = " ".join(recipie_directions)

for line in recipie_ingreds:
    new_line = nltk.tokenize.word_tokenize(line)
    quantity = new_line[0]
    measure = new_line[1]
    print (quantity + ' :: ' + measure)
print('\n\n')
print(recipie_ingreds)
#print(recipie_directions)



#sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
#directions_test = ('\n-----\n'.join(sent_detector.tokenize(recipie_directions)))
#ingred_test = ''.join(sent_detector.tokenize(recipie_ingreds))
#ingred_test = ingred_test.split('\n')
#print(directions_test)


#print(ingred_test)

#for item in ingred_test:
#    treebank = TreebankWordTokenizer()
#    ingred_tokens = treebank.tokenize(item)
#    print(ingred_tokens)

#print(ingred_tokens)

#http://www.101cookbooks.com/archives/cocagne-bean-artichoke-salad-recipe.html
#http://www.101cookbooks.com/archives/caramelized-fennel-on-herbed-polenta-recipe.html
#http://www.101cookbooks.com/archives/summer-berry-crisp-recipe.html
#http://www.101cookbooks.com/archives/avocado-asparagus-tartine-recipe.html
#http://www.101cookbooks.com/archives/goldencrusted-brussels-sprouts-recipe.html
#http://www.101cookbooks.com/archives/green-curry-dumplings-recipe.html
#http://www.101cookbooks.com/archives/a-good-shredded-salad-recipe.html
#http://www.101cookbooks.com/archives/thai-zucchini-soup-recipe.html
#http://www.101cookbooks.com/archives/mung-yoga-bowl-recipe.html