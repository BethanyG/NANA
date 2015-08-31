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
import json
from RecipeMaker import *
from server import app
from model import *
    
connect_to_db(app)

#current_recipe = RecipeMaker.parse_recipe("http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup")

class IngredientAnalyzer(object):
    
    @staticmethod
    def set_ingredient_tokens(current_recipe):
        
        for item in current_recipe.ingredients:
                quantity_conversion = {'quarter' : 0.25,'eighth' : 0.125,
                                        'half' : 0.5,'1/4' : 0.25,
                                        '1/8' : 0.125,'1/3' : 0.333,
                                        '2/3' : 0.667,'3/4' : 0.75,
                                        '1/2' : 0.5,'1' : 1.0,
                                        '2' : 2.0,'3' : 3.0,
                                        '4' : 4.0,'5' : 5.0,
                                        '6' : 6.0,'7' : 7.0, 'lots' : 2.0,
                                        '8' : 8.0,'9' : 9.0, '5-6' : 5.5,
                                        'a' : 1.0,'few' : 3.0, 'scant' : 1.0}
                
                #set 'dumb' quantity by assuming the first item is quanity
                prelim_quantity = nltk.tokenize.word_tokenize(item.source_line)[0]
                print prelim_quantity.strip(" ")                
                if quantity_conversion[prelim_quantity.strip(" ")] :
                    prelim_quantity = quantity_conversion[prelim_quantity.strip(" ")]
                else :
                    prelim_quantity = 0
                    
                item.quantity = prelim_quantity
                #print item.quantity
                #set 'dumb measurement unit by assuming the second item is units            
                item.measure = nltk.tokenize.word_tokenize(item.source_line)[1]
                #print item.measure
                #set 'dumb search term by assuming he third item is the ingredient            
                item.search_term = nltk.tokenize.word_tokenize(item.source_line)[2]
                #print item.search_term 
        
        return current_recipe
    
    
    @staticmethod
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
                Ingredient.ndb_alternates = None
    
        return Ingredient
    
    @staticmethod
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
                Ingredient.nutrition_values[row.nutrient_desc] = [float(row.value_per_portion), row.units]
        
        return Ingredient
 
    @staticmethod
    def analysis_summary(ingredients):
        analysis_summary = {}
        for item in ingredients:        
            for entry,value in item.nutrition_values.iteritems():
                #print value[0]
                analysis_summary.setdefault(entry, [0])
                analysis_summary[entry][0] = analysis_summary[entry][0] + value[0] * item.quantity
                #analysis_summary[entry][1] = value[1]
            #for entry, value in item.nutrition_values.iteritems():
            #    analysis_summary[entry][0] = analysis_summary[entry][0] + value[0]  
        
        
        return analysis_summary


#current_recipe = RecipeMaker.parse_recipe("http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup")
#IngredientAnalyzer.set_ingredient_tokens(current_recipe)

#for ingredient in current_recipe.ingredients:
#        ingredient = IngredientAnalyzer.query_for_ingredient(ingredient)

#for ingredient in current_recipe.ingredients:
#        ingredient = IngredientAnalyzer.query_for_ingredient_nutrition(ingredient)



#for ingredient in current_recipe.ingredients:  
#    ingredient = query_for_ingredient(ingredient)

#for ingredient in current_recipe.ingredients:
#    ingredient = query_for_ingredient_nutrition(ingredient)


#print(current_recipe.ingredients[1])

#print(current_recipe.ingredients)


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

