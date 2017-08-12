# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:28:15 2015

@author: bethanygarcia

"""
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import nltk
import abc
import json
import pint

class Quantity_JSONEncoder(json.JSONEncoder):
    """JSON encoder for pint.Quantity.
    """
    def default(self, obj):
        """Override the default JSONEncoder behaviour.

        Transforms pint.Quantity into dict objects for serializing. 

        Args:
            obj (any): the object to encode to JSON.
        """
        if isinstance(obj, pint.quantity._Quantity):
            return (obj.magnitude, str(obj.units))
        # Let the base class default method raise the TypeError
        return json.JSONEncoder.default(self, obj)

class Recipe(object):
    '''Represents an entire recipe after it's seperated and parsed from the 
       source URL.  Returns a Recipe object or json document.'''
    def __init__(self):
        self.sourceurl = None
        self.photo = None        
        self.title = None
        self.description = None
        self.preptime =  None
        self.cooktime = None
        
        '''This will become a list of ingredient objects,
           populated by both the parsers and the nutrient anayalizer class'''
        self.ingredients = None 

        self.directions = None
        self.servings = None
        self.analysis_summary = {}
    
    
    def make_json(self):
        '''Jsonifys a Recipe object.  Calls make_json on each ingredent
        in the ingredient list, and concatenates the results with the non-ingredient
        json.  Returns a single json documtent representing the entire Recipe.'''
        
        recipe_dict = {property : value for property, value in vars(self).items() if property != "ingredients"}        
        ingredient_list = []
        
        for item in self.ingredients:
            ingredient_list.append(Ingredient.make_json(item))
            
        recipe_json = json.dumps(recipe_dict, cls=Quantity_JSONEncoder).rstrip("}") + ',"ingredients" : [ '
        ingredient_json = ",".join(ingredient_list)        
        new_recipe_json = recipe_json + ingredient_json.lstrip("'").rstrip("'") + "]}"
        
        return new_recipe_json
 
 
    def __repr__(self):
        return "%s" % (self.__dict__)

    
    def __str__(self):
        return "%s" % (self.__dict__)

        
class Ingredient(object):
    def __init__(self, source_line):
        self.source_line = source_line
        self.db_item_match = None       #WARNING!  This is getting assigned as a TUPLE from the DB     
        self.ndb_no = None              #value filled in from query 1
        self.ndb_alternates = {}        #{ndb_no (key) : [sring for human in ui, weights.measurement_desc]}
        self.quantity = None
        self.measure = None             #once query 1 in analyzer is run, it's weights.measurement is placed here
        self.gr_weight = 100            # The gram weight. Converting factor between the measure and 100 grams.
        self.search_term = None         #if search term changes significantly as a reult of query, this will be updated
        
        '''result of the nutrient anaylizer class calling queries against the 
           USDA DB. KEY = nutrient_no, VALUE = list containing
           value per measured item, nutrient description, and nutrient units'''        
        self.nutrition_values = {} 
    
    
    def make_json(self):
        '''make json out of the Ingredient object passed in'''
        
        ingredient_json =  json.dumps({property : value for property, value in vars(self).items()})          
        
        return ingredient_json
   
   
    def __repr__(self):
        return "%s" % (self.__dict__)
        
    def __str__(self):
        return "%s" % (self.__dict__)
    
        
class RecipeMaker(object, metaclass=abc.ABCMeta):
    
    #metaclass assignment to ABCMeta(abstract class)
    '''decides which child class to call based on the hostname of the url passed in.       
       TO DO:  add case where url isn't recognized, or user hand-enters recipe.'''    
        
    @classmethod            
    def parse_recipe(cls, url):
        maker_dict = {'www.manjulaskitchen.com':ManjulasMaker,
                      'www.101cookbooks.com':OneCookMaker,
                      'www.gourmet.com':GourmetMaker}    
        target_maker = urlparse(url)[1]
        print(target_maker)
        current_maker = maker_dict[target_maker]
        
        #create child and call child's process_url method        
        current_recipe = current_maker(url).process_url()
        
        #passes back to the caller what the child class passes back        
        return current_recipe
    
    #declaring an abstract method that must be implemented in all child classes
    @abc.abstractmethod
    def process_url(self):
        '''all child makers need to implement this as their 
            main method for processing an in comming recipe url'''
    
    #init for this class & all children of this class (children have no init)
    def __init__(self, url):
        self.url = url
        self.maker_recipe = Recipe()


    
class OneCookMaker(RecipeMaker):
    '''Parser for 101cookbooks.com....one of the most dificlut sites to parse.  
       Great test for vague and non-standar language.'''
       
    def process_url(self):
        #open the URL, create a BeautfulSoup object, and create an object from the recipe div        
        html = urlopen(self.url) 
        bsObj = BeautifulSoup(html, 'html5lib')
        recipe = bsObj.find("div", {"id":"recipe"})
        filter_list = ['\n\n', '\n\n\n', '\n', ' === end recipe div === ']
        
        #set Recipe object's sourceurl and title
        self.maker_recipe.sourceurl = self.url
        self.maker_recipe.title = recipe.h1.getText().strip()
        
        #set Recipe object's description, preptime, and cooktime, IF they are found
        if recipe.p.i:    
            self.maker_recipe.description = recipe.p.i.getText().strip()
        
        if recipe.find("span", {"class":"preptime"}):
            self.maker_recipe.preptime = recipe.find("span", {"class":"preptime"}).getText().strip()
        
        if recipe.find("span", {"class":"cooktime"}):
            self.maker_recipe.cooktime = recipe.find("span", {"class":"preptime"}).getText().strip()

        #find and parse ingredients
        recipe_ingreds = [item.getText().strip() for item in recipe.blockquote.findAll('p') if item not in filter_list]
        recipe_ingreds = "\n".join(recipe_ingreds)
        recipe_ingreds = [_f for _f in recipe_ingreds if _f]
        recipe_ingreds = recipe_ingreds.split('\n')
        
        
        '''for every line in recipe_ingreds, make Ingredient object & assign the 
           line to Ingredient.source_line.  Assign the resulting list of objects 
           to Recipe.ingredients'''        
        self.maker_recipe.ingredients = [Ingredient(item) for item in recipe_ingreds]

        #find and parse directions (soooo. much. parsing.)
        recipe_directions = [item.string for item in recipe.blockquote.next_siblings if item not in filter_list]
        recipe_directions = [_f for _f in recipe_directions if _f]
        
        for item in recipe_directions:
            if "Serves" in item:
                self.maker_recipe.servings = item.string
                recipe_directions.remove(item)
            else: continue

        recipe_directions = " ".join(recipe_directions)        

        #inialize nltk sentance detector
        sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')

        #Use sentance detector further clean directions, then set Recipe.directions
        self.maker_recipe.directions = ('\n'.join(sent_detector.tokenize(recipe_directions)))
 
        #at last we are done!
        return self.maker_recipe   


              
class ManjulasMaker(RecipeMaker):
    '''parser for manjlaskitchen.com.'''
    def process_url(self):
        html = urlopen(self.url)
        bsObj = BeautifulSoup(html, 'html5lib')        
        divList = bsObj.find("div", {"class":"content-wrapper"})
        
        additional_supplies = None                 
        
        self.maker_recipe.title = bsObj.find("h1", {"class":"entry-title"}).getText().strip()
        self.maker_recipe.sourceurl = self.url

        descripts = [s.getText().strip() for s in divList.findAll('p')]
        ingreds = [s.getText().strip() for s in divList.findAll('ul')]
        directions = [s.getText().strip() for s in divList.findAll('ol')]
    
        self.maker_recipe.directions = directions[0]            
        self.maker_recipe.photo = divList.img.attrs['src']
        self.maker_recipe.description = descripts[0]
  
        for d in descripts:
            if 'will serve' in d or 'Serves' in d:
                self.maker_recipe.servings = d
                descripts.remove(d)
            if 'Preparation' in d:
                self.maker_recipe.preptime = d
                descripts.remove(d)
            if 'Cooking time' in d:
                self.maker_recipe.cooktime = d
                descripts.remove(d)
            elif 'Ingredients' or 'Method' in d:
                continue
            
        if len(ingreds) > 1:
            self.maker_recipe.ingredients = [Ingredient(item) for item in ingreds[0].split('\n')]
            additional_supplies = ingreds[1:]
            
            #BUG:  this is tossing an error on some recipies.  Need to find out why and fix
            self.maker_recipe.description += " " + additional_supplies
            
        else: self.maker_recipe.ingredients = [Ingredient(item) for item in ingreds[0].split('\n')]
        
        return self.maker_recipe
       

class AlmostTurkMaker(RecipeMaker):
    '''Placeholder stub.  Still a work in progress.'''
       
    def process_url(self):
       html = urlopen(self.url)
       bsObj = BeautifulSoup(html, 'html5lib') 
       
       pass

       
class GourmetMaker(RecipeMaker):
    '''WARNING: Not yet completely tested.  Needs to accoumodate the pre-2008
       format change.  Currently can't choose 'old'(pre 2008) recipes!'''
    
    def process_url(self):
        html = urlopen(self.url)
        bsObj = BeautifulSoup(html, 'html5lib')      
        recipe = bsObj.find("div", {"class":"recipe"})
        
        self.maker_recipe.sourceurl = self.url
        
        if bsObj.find("h1", {"class":"header"}).getText():
            self.maker_recipe.title = bsObj.find("h1", {"class":"header"}).string
        if bsObj.find("div", {"class":"text"}):
            self.maker_recipe.title = bsObj.find("div", {"class":"text"}).string
                      
        self.photo = bsObj.find("div", {"class":"w"}).img.attrs['src']
    
        if bsObj.find("div", {"class":"introduction"}):
            self.maker_recipe.description = bsObj.find("div", {"class":"introduction"}).string
        if bsObj.find("div", {"class":"text"}):
            description = [''.join(item.getText().split('<em>')) for item in bsObj.find("div", {"class":"text"}).contents]
            self.maker_recipe.description = description[0]
    
        ingreds_list = [item.getText().strip('\n') for item in bsObj.findAll("ul", {"class":"ingredients"})]
        #ingreds_list = [''.join(item.getText().split('\n')) for item in bsObj.findAll("div", {"class":"ingredient-set"})]        
        
        test_list = [item.findAll("li") for item in bsObj.findAll("ul", {"class":"ingredients"})]
        print (test_list)
        
        self.maker_recipe.ingredients = [item.strip() for item in ingreds_list]
        self.maker_recipe.directions = ''.join(bsObj.find("div", {"class":"preparation"}).getText().split('\n'))
        self.maker_recipe.servings = bsObj.find("div", {"class":"time-and-yield"}).getText().strip()
        self.maker_recipe.cooktime = ' '.join(bsObj.find("ul", {"class":"time"}).getText().split())
        
        return self.maker_recipe
