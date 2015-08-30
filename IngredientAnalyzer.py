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

def set_ingredient_tokens(current_recipe):
    
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
    
    return current_recipe



def query_for_ingredient(Ingredient):
    
    
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
    
    
    if Ingredient.search_term == None:
        return Ingredient
    
    else:    
        term, measure = Ingredient.search_term, Ingredient.measure
        #print term
        #print measure
        INGRED_QUERY = QUERY.format(ingredient=term, measurement=measure)    
        #print INGRED_QUERY 
        ingred_query_result = db.engine.execute(text(INGRED_QUERY))
        
        first_row = ingred_query_result.fetchone()     #fetches the first row and processes it differently
        
        if first_row != None:    
            Ingredient.ndb_no  = first_row[0]          #setting ndb_no for nutrition query
            Ingredient.measure = first_row[3]          #setting measure term for nutrition query
            
            Ingredient.db_item_match = first_row.ndb_no, first_row.long_desc + " " + str(first_row.amount) + first_row.measurement_desc
          
            for row in ingred_query_result:            #goes through the remaining rows in query and adds them to the alternates list      
                Ingredient.ndb_alternates[(row.measurement_desc)] = [row.ndb_no, row.long_desc + " " + str(row.amount) + row.measurement_desc]
        else:
            Ingredient.ndb_no  = None
            Ingredient.measure = None
            ingredient.ndb_alternates = None

    return Ingredient
 
def query_for_ingredient_nutrition(Ingredient):
        
    QUERY = '''SELECT 
                   nutrient_definitions.nutrient_desc,
                   round((weights.gram_weight * nutrient_data.nutrient_val / 100), 4) as Value_per_portion,
                   nutrient_definitions.units,
                   nutrient_definitions.num_decimals,
                   weights.measurement_desc,
                   nutrient_data.num_data_pts
               FROM 
                   weights
               JOIN
                   nutrient_data
                   ON weights.ndb_no = nutrient_data.ndb_no
               JOIN 
                   nutrient_definitions
                   ON nutrient_data.nutrient_no = nutrient_definitions.nutrient_no
               JOIN
                   user_nutrients
                   ON nutrient_data.nutrient_no = user_nutrients.nutrient_no and user_nutrients.user_id = 0
               WHERE
                   nutrient_data.ndb_no = '{ndb_no}' and weights.measurement_desc = '{measure}'
                   ORDER BY nutrient_definitions.nutrient_desc ASC;'''
        
    
    if Ingredient.ndb_no == None:
        return Ingredient
    
    else:
        ndb_no, measure = Ingredient.ndb_no, Ingredient.measure
        
        NUT_QUERY = QUERY.format(ndb_no=ndb_no, measure=measure) 
        nutrition_query_result = db.engine.execute(text(NUT_QUERY)) 
        
        for row in nutrition_query_result:
            Ingredient.nutrition_values[row.nutrient_desc] = [row.value_per_portion, row.units]
    
    return Ingredient
 
 
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

set_ingredients(current_recipe)

for ingredient in current_recipe.ingredients:  
    ingredient = query_for_ingredient(ingredient)

for ingredient in current_recipe.ingredients:
    ingredient = query_for_ingredient_nutrition(ingredient)


#print(current_recipe.ingredients[1])

print(current_recipe.ingredients)


#print(current_recipe.ingredients[1].nutrition_values)

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

