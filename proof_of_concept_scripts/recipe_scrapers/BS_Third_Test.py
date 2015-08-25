# -*- coding=utf_8 -*-
"""
Created on Fri Aug  7 16:10:16 2015

@author: bethanygarcia
"""


from urllib2 import urlopen
from bs4 import BeautifulSoup
import re

html = urlopen("http://www.manjulaskitchen.com/2014/04/09/carrot-ginger-soup/") 
bsObj = BeautifulSoup(html, 'html5lib')

divList = bsObj.find("div", {"class":"content-wrapper"})
#http://stackoverflow.com/questions/5615647/python-using-beautiful-
#soup-for-html-processing-on-specific-content



descripts = [s.getText().strip() for s in divList.findAll('p')]
ingreds = [s.getText().strip() for s in divList.findAll('ul')]
directions = [s.getText().strip() for s in divList.findAll('ol')]
recipie_photo = divList.img.attrs['src']
recipie_description = descripts[0]
serving_size = None
prep_time = None
cook_time = None
recipie_ingrediants = None
additional_supplies = None

for d in descripts:
    if 'will serve' in d or 'Serves' in d:
        serving_size = d
        descripts.remove(d)
    if 'Preparation' in d:
        prep_time = d
        descripts.remove(d)
    if 'Cooking time' in d:
        cook_time = d
        descripts.remove(d)
    elif 'Ingredients' or 'Method' in d:
        continue



if len(ingreds) > 1:
    ingreds[0] = recipie_ingrediants
    ingreds[1:] = additional_supplies

else: recipie_ingrediants = ingreds[0]  

for direct in directions:
        print direct
    

print recipie_photo
print recipie_description
print serving_size
print prep_time
print cook_time
print recipie_ingrediants
print additional_supplies




#for string in divList.stripped_strings:
#    print(repr(string))


#recipie_description = descripts[0]
#recipie_servings = descripts[1]
#recipie_ingredients = descripts[2] + ingreds[0]
#recipie_alsoneeded = descripts[3] + ingreds[1]
#recipie_instructions = descripts[4] + directions[0]
#recipie_notes = descripts[5].encode("UTF-8")
#recipie_notes_too = descripts[6].encode("UTF-8")
#recipie_serving_suggest = directions[1]
#recipie_substitutions = directions[2]



