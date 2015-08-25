# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 10:41:55 2015

@author: bethanygarcia

Not even close to possible without the tutorials and tips listed here:
http://www.postgresonline.com/journal/archives/169-Fuzzy-string-matching-with-Trigram-and-Trigraphs.html

Equally impossible without the tips here and here:
http://stackoverflow.com/questions/12413705/parsing-natural-language-ingredient-quantities-for-recipes
http://stackoverflow.com/questions/6115677/english-grammar-for-parsing-in-nltk
http://www.clips.ua.ac.be/pattern
http://www.clips.ua.ac.be/pages/pattern-en#tree

Also did extensive reading and testing with nltk.  But the stanford parser was too slow:
http://www.nltk.org/book/
http://www.nltk.org/api/nltk.parse.html
http://nbviewer.ipython.org/github/gmonce/nltk_parsing/blob/master/1.%20NLTK%20Syntax%20Trees.ipynb

"""

from pattern.en import parsetree
from pattern.en import pluralize, singularize
#from pattern.search import search
#from pattern.search import search, taxonomy
#from pattern.search import match
from RecipeMaker import *
from model import *

current_recipe = RecipeMaker.parse_recipe("http://www.101cookbooks.com/archives/avocado-asparagus-tartine-recipe.html")

def set_ingredients(current_recipe):
    
    for item in current_recipe.ingredients:
            #set 'dumb' quantity by assuming the first item is quanity
            item.quantity = nltk.tokenize.word_tokenize(item.source_line)[0]
            #make parse tree out of ingredient line            
            sentence = parsetree(item.source_line, chunks=True, lemmata=True)
            
            for s in sentence:
                #filter all the NP (noun phrases) into a chunk list
                chunk_list = [singularize(chunk.string) for chunk in s.chunks if chunk.type =='NP']
                #set the best guess on measurement                
                item.measure = chunk_list[0]            
                #set best guess on db search term
                if len(chunk_list) > 1:
                    search_term = chunk_list[1]
                else: search_term = chunk_list[0]
                item.search_term = str(search_term)


def perform_search(current_recipe):
    






#chunk_list = []
#for s in sentence:
#    for chunk in s.chunks:
#        if chunk.type =='NP':
#            chunk_list.append(chunk.string)
#        print '\n'        
        #print [w.string for w in chunk if chunk.type == 'NP']




#print chunk_list_II
#print current_recipe.ingredients[0].quantity
    
for ingredient in current_recipe.ingredients:
    print(ingredient)
#    print('QUANTITY::: ' + ingredient.quantity)
#    print('MEASURE::: ' + ingredient.measure)
#    print('SEARCH TERM:: ' + ingredient.search_term)
#    print('\n')
    