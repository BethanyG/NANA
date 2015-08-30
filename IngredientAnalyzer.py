# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:22:31 2015

@author: bethanygarcia

Not even close to possible without the tutorials and tips listed here:
http://www.postgresonline.com/journal/archives/169-Fuzzy-string-matching-with-Trigram-and-Trigraphs.html
http://stackoverflow.com/questions/11249635/finding-similar-strings-with-postgresql-quickly

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
from server import app
from model import *
    
connect_to_db(app)

current_recipe = RecipeMaker.parse_recipe("http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup")

def set_ingredients(current_recipe):
    
    for item in current_recipe.ingredients:
            #set 'dumb' quantity by assuming the first item is quanity
            item.quantity = nltk.tokenize.word_tokenize(item.source_line)[0]
            #print item.quantity
            #set 'dumb measurement unit by assuming the second item is units            
            item.measure = nltk.tokenize.word_tokenize(item.source_line)[1]
            #print item.measure
            #set 'dumb search term by assuming he third item is the ingredient            
            item.search_term = nltk.tokenize.word_tokenize(item.source_line)[2]
            #print item.search_term 
    
   
    
    QUERY = '''SELECT
                	food_descriptions.ndb_no, food_descriptions.long_desc, 
                   weights.amount, weights.measurement_desc, weights.gram_weight, 
                   similarity(food_descriptions.long_desc, '{ingredient}') AS sim_score, 
                   similarity(weights.measurement_desc, '{measurement}') AS sim_score_measure
        FROM
        		food_descriptions
        JOIN
        		weights ON food_descriptions.ndb_no = weights.ndb_no
        WHERE
        		food_descriptions.long_desc % '{ingredient}' 
        		AND 
        			similarity(food_descriptions.long_desc, '{ingredient}') > 0.35
        		AND 
        			similarity(weights.measurement_desc, '{measurement}') > 0.035;'''
    
    
    term = "carrots"
    #print term
    measure = "cups"
    #print measure
    TEST_Q = QUERY.format(ingredient=term, measurement=measure)    
    print TEST_Q 
    test = db.engine.execute(text(TEST_Q))
    
    for row in test:
        print row.long_desc
    #print QUERY
    #test2 = db.engine.execute(text(TEST.format(ingredient="asparagus", measurement="spear"))) 
    #test = db.session.query(Food_Descriptions).from_statement(QUERY)
    
    

    #return current_recipe
 
 
 
 
'''
***************Someday, I will get this working.  Today is not that day***************  

#now make parse tree out of ingredient line            
sentence = parsetree(item.source_line, chunks=True, lemmata=True)

for s in sentence:
    #filter all the NP (noun phrases) into a chunk list
    chunk_list = [singularize(chunk.string) for chunk in s.chunks if chunk.type =='NP']
    print(chunk_list)                
    #set the best guess on measurement                
    #item.measure = chunk_list[0]            
    #set best guess on db search term
    if len(chunk_list) > 1:
        search_term = chunk_list[1]
    else: search_term = chunk_list[0]
    item.search_term = str(search_term)
'''

#return current_recipe
#def perform_search(current_recipe):

set_ingredients(current_recipe)

#for item in current_recipe.ingredients:
#    print (item.__dict__)    


#for item in current_recipe.ingredients:    
#    print ("QUANTITY::  " +  item.quantity)
#    print ("MEASURE:: " +  item.measure)
#    print ("SEARCH TERM::" + item.search_term)





#chunk_list = []
#for s in sentence:
#    for chunk in s.chunks:
#        if chunk.type =='NP':
#            chunk_list.append(chunk.string)
#        print '\n'        
        #print [w.string for w in chunk if chunk.type == 'NP']




#print chunk_list_II
#print current_recipe.ingredients[0].quantity
    
#for ingredient in current_recipe.ingredients:
#    print(ingredient)
#    print('QUANTITY::: ' + ingredient.quantity)
#    print('MEASURE::: ' + ingredient.measure)
#    print('SEARCH TERM:: ' + ingredient.search_term)
#    print('\n')

