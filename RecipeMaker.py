# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:28:15 2015

@author: bethanygarcia

Thank you Bob for all your object-oriented counseling (even if it was Java centric)!

Thank you StackOverflow! http://stackoverflow.com/questions/5615647/
python-using-beautiful-soup-for-html-processing-on-specific-content

http://stackoverflow.com/questions/3271478/check-list-of-words-in-another-string
http://stackoverflow.com/questions/1436703/difference-between-str-and-repr-in-python


Classes for creating Recipes and Ingredients.
 --Recipes have a method to JSONify themselves
 --Ingredients havea method to JSONify themselves

Classes for returning a filled Recipe object.
Sublclasses for custom webscrappers targeted for each website.  

Each parser :
    1) instantiates a Recipe object, 
    2) parses the recipe into parts, 
    3) instantiates and partially populates an array of Ingredient objects, 
    4) returns a completed Recipe object containing: 
        * a list of Ingredient objects, one per ingredient line in recipe
        * data attributes for title, source url, photo, description, preptime, 
          cooktime, servings, and directions (where each is available)
"""

from __future__ import print_function, division
from urllib2 import urlopen, urlparse
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import nltk
import abc
import json
import pickle
import inspect




class Recipe(object):
    def __init__(self):
        self.sourceurl = None
        self.photo = None        
        self.title = None
        self.description = None
        self.preptime =  None
        self.cooktime = None
        
        '''eventually, this will contain an ingredient object,
           populated by both the parsers and the nutrient anayalizer class'''
        self.ingredients = None 

        self.directions = None
        self.servings = None
    
    
    def make_json(self):
        '''doing this the sloppy, manual way to json because jsonpickle kept failing 
           with too many recursive calls. TO DO:  Clean up the ugly!  
           There *has* to be a more elegant way to get this thing jsonified.  
           Really.'''
        
        recipe_dict = {property : value for property, value in vars(self).iteritems() if property != "ingredients"}        
        ingredient_list = []
        
        for item in self.ingredients:
            ingredient_list.append(Ingredient.make_json(item))
            
        recipe_json = json.dumps(recipe_dict).rstrip("}") + ',"ingredients" : [ '
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
        self.ndb_no = None
        self.ndb_alternates = None
        self.quantity = None
        self.measure = None
        self.search_term = None
        
        '''result of the nutrient anaylizer class calling queries against the 
           USDA DB. KEY = nutrient_no, VALUE = list containing
           value per measured item, nutrient description, and nutrient units'''        
        self.nutrition_values = {}
    
    
    def make_json(self):
        '''make json out of the Ingredient object passed in'''
        
        ingredient_json =  json.dumps({property : value for property, value in vars(self).iteritems()})          
        
        return ingredient_json
   
   
    def __repr__(self):
        return "%s" % (self.__dict__)
        
    def __str__(self):
        return "%s" % (self.__dict__)
    
        
class RecipeMaker(object):
    
    #metaclass assignment to ABCMeta(abstract class)
    __metaclass__ = abc.ABCMeta    
    
    '''factory method that doesn't require an instance
       decides which child class to call based on the hostname of the url passed in.       
       TO DO:  add case where url isn't recognized, or user hand-enters recipe.'''
    @classmethod        
    def parse_recipe(cls, url):
        maker_dict = {'www.manjulaskitchen.com':ManjulasMaker,
                      'www.101cookbooks.com':OneCookMaker,
                      'almostturkish.blogspot.com':AlmostTurkMaker}    
        target_maker = urlparse.urlsplit(url)[1]
        current_maker = maker_dict[target_maker]
        
        #create child and call child's process_url method        
        current_recipe = current_maker(url).process_url()
        
        #passes back to the caller what the called child class passes back        
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
        filter_list = [u'\n\n', u'\n\n\n', u'\n', ' === end recipe div === ']
        
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
        recipe_ingreds = filter(None, recipe_ingreds)
        recipe_ingreds = recipe_ingreds.split('\n')
        
        '''for every line in recipe_ingreds, make Ingredient object & assign the 
           line to Ingredient.source_line.  Assign the resulting list of objects 
           to Recipe.ingredients'''        
        self.maker_recipe.ingredients = [Ingredient(item) for item in recipe_ingreds]

        #find and parse directions (soooo. much. parsing.)
        recipe_directions = [item.string for item in recipe.blockquote.next_siblings if item not in filter_list]
        recipe_directions = filter(None, recipe_directions)
        
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
            #self.maker_recipe.ingredients = ingreds[0]
            additional_supplies = ingreds[1:]
            self.maker_recipe.description += " " + additional_supplies
            
        else: self.maker_recipe.ingredients = [Ingredient(item) for item in ingreds[0].split('\n')]
        
        return self.maker_recipe
       
class AlmostTurkMaker(RecipeMaker):
    '''parser for almostturkish.com.  Closer to almostmademeinsane.com.
       Still not working correctly.  Sigh.'''
       
       
class GourmetMaker(RecipeMaker):
    '''parser for gourmet.com.  More or less working...just don't choose 'old'
       (pre 2007) recipes!  Isn't it lovely when site formats change??'''
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
    #directions = ''.join(bsObj.find("div", {"class":"preparation"})


#current_recipe = RecipeMaker.parse_recipe("http://www.101cookbooks.com/archives/caramelized-fennel-on-herbed-polenta-recipe.html")
#ingredients_list = current_recipe.ingredients
#current_recipe.ingredients = None
#recipe_json = json.dumps({property : value for property, value in vars(current_recipe).iteritems() if property != "ingredients"})


#for item in current_recipe.ingredients:
#    ingredient_json = json.dumps({property : value for property, value in vars(item).iteritems()})
#    print (ingredient_json)

#print(Recipe.make_json(current_recipe))

#print (recipe_json.rstrip("}"))


#for item in new_recipe:
#    print(type(item))

#print (new_recipe)




#recipe_details = RecipeMaker.make_recipe_json(current_recipe)

#for ingredient in current_recipe.ingredients:
#    ingredient = json.dumps(ingredient.__dict__)   

#new_recipe = json.dumps(current_recipe)

#recipe_test = json.dumps(new_recipe)


#print (type(new_recipe))
#print (new_recipe)   
#print(current_recipe)
#recipe_details = RecipeMaker.make_recipe_json(current_recipe)
#print(recipe_details)
#print(current_recipe)
#print ('OBJECT RECIEIVED!!!\n' + current_recipe.title + '\n')

#for item in current_recipe.ingredients:
#    print(item.source_line)

#print ('\n')
#print (current_recipe.directions)
#print (current_recipe.description)

#print (json.dumps((vars(current_recipe)), sort_keys=True, indent=4))

#frozentest = jsonpickle.encode(current_recipe, keys=True)
#thawedtest = jsonpickle.decode(frozentest)
#assert current_recipe.title == thawedtest.title
#print(frozentest)

