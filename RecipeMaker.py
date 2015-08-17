# -*- coding: utf-8 -*-
"""
Created on Thu Aug 13 16:28:15 2015

@author: bethanygarcia

Thank you Bob for all your object-oriented counseling (even if it was Java centric)!

Thank you StackOverflow! http://stackoverflow.com/questions/5615647/
python-using-beautiful-soup-for-html-processing-on-specific-content

Classes for creating Recipes and Ingredients.  
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
import nltk, re, pprint
import abc



class Recipe(object):
    def __init__(self):
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
        
    def __repr__():
        #TO DO!!!
        pass

        
class Ingredient(object):
    def __init__(self, source_line):
        self.source_line = source_line
        self.ndb_no = None
        
        '''result of the nutrient anaylizer class calling queries against the 
           USDA DB. KEY = nutrient_no, VALUE = list containing
           value per measured item, nutrient description, and nutrient units'''        
        self.nutrition_values = {}
    
    def __repr__():
        #TO DO!!
        pass
    
        
class RecipeMaker(object):
    
    #metaclass assignment to ABCMeta(abstract class)
    __metaclass__ = abc.ABCMeta    
    
    '''factory method that doesn't require an instance
       decides which child class to call based on the hostname of the url passed in.       
       TO DO:  add case where url isn't recognized, or user hand-enters recipe.'''
    @classmethod        
    def parse_recipe(self, url):
        maker_dict = {'www.manjulaskitchen.com':ManjulasMaker,
                      'www.101cookbooks.com':OneCookMaker,
                      'almostturkish.blogspot.com':AlmostTurkMaker}    
        target_maker = urlparse.urlsplit(url)[1]       
        current_maker = maker_dict[target_maker]
        
        #create chiled and call child's process_url method        
        current_recipe = current_maker(url).process_url()
        
        #passes back to the caller what the called child class passes back
        return current_recipe
    
    #declaring an abstract method that must be implemented in all child classes
    @abc.abstractmethod
    def process_url(self):
        pass
    
    #init for this class & all children of this class (children have no init)
    def __init__(self, url):
        self.url = url
        self.maker_recipe = Recipe()


    
class OneCookMaker(RecipeMaker):
        
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
    def process_url(self):
        html = urlopen(self.url)
        bsObj = BeautifulSoup(html, 'html5lib')        
        divList = bsObj.find("div", {"class":"content-wrapper"})
        
        additional_supplies = None                 
        
        self.maker_recipe.title = 'MANJULA_PLACEHOLDER'
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
            self.maker_recipe.ingredients = ingreds[0]
            additional_supplies = ingreds[1:]
            self.maker_recipe.description += " " + additional_supplies
            
        else: self.maker_recipe.ingredients = ingreds[0]  
        
        return self.maker_recipe
       
class AlmostTurkMaker(RecipeMaker):
    def __init__(self, url):
        pass
    
  
current_recipe = RecipeMaker.parse_recipe("http://www.101cookbooks.com/archives/avocado-asparagus-tartine-recipe.html")
#current_recipe = RecipeMaker.parse_recipe("http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup/")

print ('OBJECT RECIEIVED!!!\n' + current_recipe.title + '\n')

for item in current_recipe.ingredients:
    print(item.source_line)

print ('\n')
print (current_recipe.directions)
print (current_recipe.description)
