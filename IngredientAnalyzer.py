# -*- coding: utf-8 -*-
"""
Created on Mon Aug 24 17:22:31 2015

@author: bethanygarcia

"""
from collections import defaultdict
from fractions import Fraction

import nltk
import sklearn_crfsuite
from pint import UnitRegistry
import pint

from model import db

ureg = UnitRegistry()
ureg.define('IU = [vitamin]')
#current_recipe = RecipeMaker.parse_recipe("http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup")


class IngredientAnalyzer(object):
    
    @staticmethod
    def analyze_recipe(current_recipe):
        # 0. Create the parse tree from the ingredient description
        # 1. Find the whole ingredient name by concatenating the INGREDIENT names
        # from the Tree. Query the DB to find the best suitable ingredient name 
        # using maybe additional information from the COM labels.
        # 2. Find the UNIT used for this ingredient and determine if the DB 
        # supports it.
        # 3. Find the quantity by converting all the QTY strings into floating 
        # point numbers and summing them up. So that "1", "1/2" should be 
        # converted to 1.5.

        
        for ingredient in current_recipe.ingredients:
            tree = IngredientAnalyzer.parse_ingredient(ingredient.source_line)
            ingredient.search_term = IngredientAnalyzer.determine_search_term(tree)
            IngredientAnalyzer.query_for_ingredient(ingredient)
            if ingredient.ndb_no is None:
                continue
            IngredientAnalyzer.determine_weight_unit(tree, ingredient)
            IngredientAnalyzer.query_for_ingredient_nutrition(ingredient)
        
        current_recipe.analysis_summary = IngredientAnalyzer.analysis_summary(current_recipe.ingredients)
        
        return current_recipe
    
    @staticmethod
    def parse_ingredient(ingredient):
        """Parse the ingredient string.

        Returns the Tree representation of this ingredient.
        """
        crf = sklearn_crfsuite.CRF(
            model_filename='ingredient_model.crfsuite'
        )
        ingredient = normalize(ingredient)
        tok = nltk.word_tokenize(ingredient)
        pos = nltk.pos_tag(tok)
        labels = crf.predict_single(sent2features(pos))
        grammar = r"""
        AMOUNT: {<QTY>+<UNIT>?}
        INGREDIENT: {<NAME>+}
        """
        cp = nltk.RegexpParser(grammar)
        tree = cp.parse(list(zip(tok, labels)))

        return tree

    @staticmethod
    def determine_search_term(tree):
        """Determine the ingredient name from the parsed tree.

        At the moment, just take the first occurence of INGREDIENT label.
        """
        for subtree in tree.subtrees(filter=lambda t: t.label() == "INGREDIENT"):
            terms = " ".join(ingredient for ingredient, _ in subtree.leaves())
            return terms

    @staticmethod
    def determine_weight_unit(tree, ingredient):
        """Determine the weight unit from this tree for the current ingredient

        First check if unit is a mass unit. If so assign it to the ingredient
        measure.
        Second query the DB to check what units are available and try to match
        """
        amount = next(tree.subtrees(filter=lambda t: t.label()=="AMOUNT"))
        com = " ".join(s for s, label in tree.leaves() if label=="COM")
        ingredient.quantity, unit = parse_amount_tree(amount)
        unit = ureg.parse_expression(unit)
        if unit.dimensionality == ureg.gram.dimensionality:
            ingredient.measure = unit.to('grams').magnitude
        elif unit.dimensionality == ureg.liter.dimensionality:
            # Using the COM labels can help finding the correct weight unit
            db_unit, mult, gr_weight = find_db_weight_unit(ingredient.ndb_no, unit, com)
            mult = float(mult)
            gr_weight = float(gr_weight)
            ingredient.measure = str(db_unit.units)
            ingredient.gr_weight = gr_weight / mult


    @staticmethod
    def set_ingredient_tokens(current_recipe):
        """Sets the quantity, unit and ingredient name for the recipe.
        """
        for item in current_recipe.ingredients:
            # Find the quantity
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
                print(("Can't convert :: " + prelim_quantity))
                pass  # pass to conversion dictionary lookup
                try:
                    prelim_quantity = quantity_conversion[prelim_quantity]
                except KeyError:
                    print((KeyError("No conversion value found : " +  prelim_quantity)))
                    #need to flag here for note in UI                    
                    prelim_quantity = 0
                else:
                    item.quantity = prelim_quantity
            
            item.quantity = prelim_quantity
        
            filterList = ['tsp', 'tsps', 'tbsps', 'tbsp', 'tablespoon', \
                          'tablespoons', 'teaspoon', 'teaspoons', 'cup', \
                          'cups', 'bowl', 'pint', 'quart', 'mg', 'g', 'gram',\
                          'grams', 'ml', 'oz', 'ounce', 'ounces' ] 
            units = [
                {'tsp', 'tsps', 'teaspoon', 'teaspoons'},
            ]
            
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
    def query_for_ingredient(ingredient):
        
        QUERY = '''
                SELECT 
                    food_descriptions.ndb_no, food_descriptions.long_desc,
                    similarity(food_descriptions.long_desc, %s) AS sim_score  
                FROM 
                    food_descriptions
                WHERE 
                    long_desc %% %s
                AND 
                    long_desc @@ plainto_tsquery('english', %s)   
                ORDER BY 
                    food_descriptions.long_desc <-> %s;
                '''        
                
        if ingredient.search_term == None:
            return ingredient
        
        else:
            term = ingredient.search_term
            ingred_query_result = db.engine.execute(QUERY, (term, term, term, term))
            first_row = ingred_query_result.fetchone()     #fetches the first row and processes it differently
            
            if first_row != None:    
                ingredient.ndb_no  = first_row[0]          #setting ndb_no for nutrition query
                
                ingredient.db_item_match = first_row.ndb_no, first_row.long_desc
              
                # for row in ingred_query_result:            #goes through the remaining rows in query and adds them to the alternates list      
                #     ingredient.ndb_alternates[(row.measurement_desc)] = [row.ndb_no, row.long_desc + " " + str(row.amount) + row.measurement_desc]
            else:
                ingredient.ndb_no  = None
                ingredient.measure = None
                ingredient.ndb_alternates = None
    
        return ingredient
    
    @staticmethod    
    def query_for_ingredient_nutrition(ingredient):
            
        QUERY = '''\
                SELECT 
                   nutrient_definitions.nutrient_desc,
                   nutrient_data.nutrient_val,
                   nutrient_definitions.units
                FROM 
                   nutrient_data
                JOIN 
                   nutrient_definitions
                   ON nutrient_data.nutrient_no = nutrient_definitions.nutrient_no
                WHERE
                   nutrient_data.ndb_no = %s
                   ORDER BY nutrient_definitions.nutrient_desc ASC;'''
            
        if ingredient.ndb_no == None:
            return ingredient
        else:
            ndb_no = ingredient.ndb_no
            nutrition_query_result = db.engine.execute(QUERY, (ndb_no)) 
            
            for row in nutrition_query_result:
                ingredient.nutrition_values[row.nutrient_desc] = (float(row.nutrient_val), row.units)
        
        return ingredient
 
   
    @staticmethod    
    def analysis_summary(ingredients):
        n_lable_trans = {'Protein' : 'valueProteins',
                         'Total lipid (fat)' : 'valueTotalFat',
                         'Carbohydrate, by difference' : 'valueTotalCarb',
                         'Energy' : 'valueCalories',
                         'Sugars, total' : 'valueSugars',
                         'Fiber, total dietary' : 'valueFibers',
                         'Calcium, Ca' : 'valueCalcium',
                         'Iron, Fe' : 'valueIron',
                         'Magnesium, Mg' : 'valueMagnesium',
                         'Phosphorus, P' : 'valuePhosphorus',
                         'Potassium, K' : 'valuePotassium',
                         'Sodium, Na' : 'valueSodium',
                         'Zinc, Zn' : 'valueZinc',
                         'Vitamin A, IU' : 'valueVitaminA',
                         'Vitamin E (alpha-tocopherol)' : 'valueVitaminE',
                         'Vitamin D' : 'valueVitaminD',
                         'Thiamin' : 'valueThiamin',
                         'Riboflavin' : 'valueRiboflavin',
                         'Niacin' : 'valueNiacin',
                         'Pantothenic acid' : 'valuePantothenicAcid',
                         'Vitamin B-6' : 'valueVitaminB6',
                         'Vitamin B-12' : 'valueVitaminB12',
                         'Vitamin K (phylloquinone)' : 'valueVitaminK',
                         'Folate, DFE' : 'valueFolate'
                         }
        summary =   defaultdict(int)
        for item in ingredients:        
            for entry, (value, unit) in item.nutrition_values.items():
                if entry not in n_lable_trans:
                    continue
                # HACK HACK due to wrong DB collation here
                if unit == "Âµg":
                    unit = unit[1:]
                value = value * ureg.parse_expression(unit)
                # val, current_unit = summary[n_lable_trans[entry]]
                # if current_unit and current_unit != unit:
                #     raise ValueError("Trying to add nutrient {} with different units."
                #         " Old unit {}, New unit {}".format(entry, current_unit, unit))
                summary[n_lable_trans[entry]] += item.quantity * value / 100 * item.gr_weight
        return summary

def normalize(ingredient):
    "Normalizes the string"
    return ingredient.lower()

def word2features(sent, i):

    features = []
    if i >= 2:
        word_2, postag_2, *_ = sent[i-2]
        features.append('w[-2]=' + word_2)
    if i >= 1:
        word_1, postag_1, *_ = sent[i-1]
        features.append('w[-1]=' + word_1)
    word, postag, *_ = sent[i]
    features.append('w[0]=' + word)
    if i < len(sent)-1:
        word_1a, postag_1a, *_ = sent[i+1]
        features.append('w[+1]=' + word_1a)
    if i < len(sent)-2:
        word_2a, postag_2a, *_ = sent[i+2]
        features.append('w[+2]=' + word_2a)
    if i >= 1:
        features.append('w[-1]|w[0]=' + word_1 + "|" + word)
    if i < len(sent)-1:
        features.append('w[0]|w[+1]=' + word + "|" + word_1a)
    # POS
    if i >= 2:
        features.append('pos[-2]=' + postag_2)
    if i >= 1:
        features.append('pos[-1]=' + postag_1)
    features.append('pos[0]=' + postag)
    if i < len(sent)-1:
        features.append('pos[+1]=' + postag_1a)
    if i < len(sent)-2:
        features.append('pos[+2]=' + postag_2a)

    if i >= 2:
        features.append('pos[-2]|pos[-1]=' + postag_2 + "|" + postag_1)
    if i >= 1:
        features.append('pos[-1]|pos[0]=' + postag_1 + "|" + postag)
    if i < len(sent)-1:
        features.append('pos[0]|pos[1]=' + postag + "|" + postag_1a)
    if i < len(sent)-2:
        features.append('pos[1]|pos[2]=' + postag_1a + "|" + postag_2a)
    if i >= 2:
        features.append('pos[-2]|pos[-1]|pos[0]=' + postag_2 + "|" + postag_1 + "|" + postag)
    if i >= 1 and i < len(sent)-1:
        features.append('pos[-1]|pos[0]|pos[1]=' + postag_1 + "|" + postag + "|" + postag_1a)
    if i < len(sent)-2:
        features.append('pos[0]|pos[1]|pos[2]=' + postag + "|" + postag_1a + "|" + postag_2a)

    if i == 0:
        features.append('__BOS__')
        
    if i == len(sent)-1:
        features.append('__EOS__')
                
    return features

def sent2features(sent):
    return [word2features(sent, i) for i in range(len(sent))]

def parse_amount_tree(tree):
    "Parse the tree to find the total quantity and the unit used"
    quantity = 0
    unit = ""
    for value, label in tree.leaves():
        if label == "QTY":
            quantity += str_to_float(value)
        elif label == "UNIT":
            unit = value
    return quantity, unit

def str_to_float(s):
    try:
        q = float(s)
    except ValueError:
        try:
            f = Fraction(s)
            q = float(f)
        except ValueError:
            raise ValueError("{} cannot be parsed as a float".format(s))
    return q

def find_db_weight_unit(ndb_no, unit, com):
    """Query the DB to find an equivalent unit of measurement.
    """
    QUERY = '''\
        SELECT
            weights.measurement_desc, weights.amount, weights.gram_weight,
            similarity(weights.measurement_desc, %s) AS sim_score 
        FROM
            weights
        WHERE
            weights.ndb_no = %s
        ORDER BY 
            sim_score DESC;'''

    query_result = db.engine.execute(QUERY, (str(unit.units) + " " + com, ndb_no))
    for row in query_result:
        try:
            first_word = row.measurement_desc.split()[0]
            db_unit = ureg.parse_expression(first_word)
        except pint.errors.UndefinedUnitError:
            continue
        if db_unit.dimensionality == unit.dimensionality:
            return unit.to(db_unit), row.amount, row.gram_weight
    raise ValueError("Cannot find {} as a weight unit in the DB.".format(unit.units))
    

if __name__ == '__main__':
    from server import app
    from model import connect_to_db
    from RecipeMaker import Ingredient, Recipe
    
    connect_to_db(app)

    recipe = Recipe()
    ingredient = Ingredient("1/3 cup ginger peeled and cut in small pieces")
    recipe.ingredients = [ingredient]
    IngredientAnalyzer.analyze_recipe(recipe)
