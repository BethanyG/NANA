# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:22:31 2015

@author: bethanygarcia

"""
import pattern3
#from pattern.en import parsetree
#from pattern.en import pluralize, singularize
import json
from RecipeMaker import *
from server import app
from model import *
    
connect_to_db(app)

#current_recipe = RecipeMaker.parse_recipe("http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup")


class IngredientAnalyzer(object):
    
    @staticmethod
    def analyze_recipe(current_recipe):
        IngredientAnalyzer.set_ingredient_tokens(current_recipe)
        
        for ingredient in current_recipe.ingredients:
            IngredientAnalyzer.query_for_ingredient(ingredient)
            IngredientAnalyzer.query_for_ingredient_nutrition(ingredient)

        
        current_recipe.analysis_summary = IngredientAnalyzer.analysis_summary(current_recipe.ingredients)
        
        return current_recipe
    
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
                                    '6' : 6.0,'7' : 7.0, 'lots' : 3.0,
                                    '8' : 8.0,'9' : 9.0, '5-6' : 5.5,
                                    'a' : 1.0,'few' : 2.0, 'scant' : 1.0, 
                                    'pinch' : 0.125, 'pinches' : 0.25, 
                                    '4-' : 4.0, 'to' : 0.0, 'tablespoon' : 1.0, 
                                    'teaspoon' : 1.0, 'couple' : 2.0}
                    
            #set 'dumb' quantity by assuming the first item is quanity
            prelim_quantity = nltk.tokenize.word_tokenize(item.source_line)[0]
            
            #EAFP!
            try:
                prelim_quantity = float(prelim_quantity)
            except ValueError:
                print("Can't convert :: " + prelim_quantity)
                pass  # pass to conversion dictionary lookup
                try:
                    prelim_quantity = quantity_conversion[prelim_quantity]
                except KeyError:
                    print (KeyError("No conversion value found : " +  prelim_quantity))
                    #need to flag here for note in UI                    
                    prelim_quantity = 0
                else:
                    item.quantity = prelim_quantity
            
            item.quantity = prelim_quantity
        
            filterList = ['tsp', 'tsps', 'tbsps', 'tbsp', 'tablespoon', \
                          'tablespoons', 'teaspoon', 'teaspoons', 'cup', \
                          'cups', 'bowl', 'pint', 'quart', 'mg', 'g', 'gram',\
                          'grams', 'ml', 'oz', 'ounce', 'ounces' ] 
            
            item.measure = ' '.join([word for word in item.source_line.split(" ") if word in filterList])
            new_source_line = ' '.join([word for word in item.source_line.split(" ") if word not in filterList])                               
            sentence = parsetree(new_source_line, chunks=True, lemmata=True)
         
            for s in sentence:
                #filter all the NP (noun phrases) into a chunk list
                chunk_list = [singularize(chunk.string) for chunk in s.chunks if chunk.type =='NP']
                search_term = chunk_list[0]
                search_term = "".join([i for i in search_term if i != '/'])
                search_term = ''.join([i for i in search_term if not i.isdigit()])                
                
                item.search_term = search_term
    
        return current_recipe
   
    @staticmethod
    def query_for_ingredient(Ingredient):
        
        
        QUERY = '''SELECT
                        food_descriptions.ndb_no, food_descriptions.long_desc, weights.amount, 
                        weights.measurement_desc, weights.gram_weight, 
                        similarity(food_descriptions.long_desc, %s) AS sim_score, 
                        similarity(weights.measurement_desc, %s) AS sim_score_measure
                   FROM
                        food_descriptions
                   JOIN
                        weights ON food_descriptions.ndb_no = weights.ndb_no
                   WHERE
                        long_desc @@ plainto_tsquery('english', %s)
                   AND 
                        similarity(weights.measurement_desc, %s) > 0.035
                   ORDER BY 
                        similarity(food_descriptions.long_desc, %s) > 0.35 DESC;'''
        
        if Ingredient.search_term == None:
            return Ingredient
        
        else:    
            term, measure = Ingredient.search_term, Ingredient.measure
            ingred_query_result = db.engine.execute(QUERY, (term, measure, term, measure, term))
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
                       nutrient_data.ndb_no = %s and weights.measurement_desc = %s
                       ORDER BY nutrient_definitions.nutrient_desc ASC;'''
            
        
        if Ingredient.ndb_no == None:
            return Ingredient
        
        else:
            ndb_no, measure = Ingredient.ndb_no, Ingredient.measure
            nutrition_query_result = db.engine.execute(QUERY, (ndb_no, measure)) 
            
            for row in nutrition_query_result:
                Ingredient.nutrition_values[row.nutrient_desc] = [float(row.value_per_portion), row.units]
        
        return Ingredient
 
   
    @staticmethod    
    def analysis_summary(ingredients):
        analysis_summary =   {}
        for item in ingredients:        
            for entry,value in item.nutrition_values.iteritems():
                analysis_summary.setdefault(entry, [0])
                analysis_summary[entry][0] = analysis_summary[entry][0] + value[0] * item.quantity
        
            
        n_lable_trans = {u'Protein' : 'valueProteins',
                         u'Total lipid (fat)' : 'valueTotalFat',
                         u'Carbohydrate, by difference' : 'valueTotalCarb',
                         u'Energy' : 'valueCalories',
                         u'Sugars, total' : 'valueSugars',
                         u'Fiber, total dietary' : 'valueFibers',
                         u'Calcium, Ca' : 'valueCalcium',
                         u'Iron, Fe' : 'valueIron',
                         u'Magnesium, Mg' : 'valueMagnesium',
                         u'Phosphorus, P' : 'valuePhosphorus',
                         u'Potassium, K' : 'valuePotassium',
                         u'Sodium, Na' : 'valueSodium',
                         u'Zinc, Zn' : 'valueZinc',
                         u'Vitamin A, IU' : 'valueVitaminA',
                         u'Vitamin E (alpha-tocopherol)' : 'valueVitaminE',
                         u'Vitamin D' : 'valueVitaminD',
                         u'Thiamin' : 'valueThiamin',
                         u'Riboflavin' : 'valueRiboflavin',
                         u'Niacin' : 'valueNiacin',
                         u'Pantothenic acid' : 'valuePantothenicAcid',
                         u'Vitamin B-6' : 'valueVitaminB6',
                         u'Vitamin B-12' : 'valueVitaminB12',
                         u'Vitamin K (phylloquinone)' : 'valueVitaminK',
                         u'Folate, DFE' : 'valueFolate'
                         }
        
        new_analysis_summary = {n_lable_trans[key] : value[0] for (key, value) in analysis_summary.iteritems()}
        
        return new_analysis_summary
