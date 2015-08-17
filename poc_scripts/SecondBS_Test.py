# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 17:10:13 2015

@author: bethanygarcia
"""

from urllib2 import urlopen
from bs4 import BeautifulSoup
import re
html = urlopen("http://www.manjulaskitchen.com/2008/04/06/chola-tikki/") 
bsObj = BeautifulSoup(html, 'lxml')

divList = bsObj.find("div", {"class":"content-wrapper"})
#http://stackoverflow.com/questions/5629773/
#python-html-parsing-with-beautiful-soup-and-filtering-stop-words

descripts = [s.getText().strip() for s in divList.findAll('p')]
ingreds = [s.getText().strip() for s in divList.findAll('ul')]
directions = [s.getText().strip() for s in divList.findAll('ol')]
recipie_photo = divList.findAll("img", {"src":re.compile("\.jpg")})

#for child in bsObj.find("div",{"class":"content-wrapper"}).children:
#    print(child)



recipie_description = descripts[0]
recipie_servings = descripts[1]



print 'DESCRIPTION::' + str(recipie_description)
print 'SERVINGS::' + str(recipie_servings)
print 'PHOTO::' + str(recipie_photo[0])


for d in descripts:
    print d
    
for ingred in ingreds:
    print ingred  

print 'DIRECTIONS::'

for direct in directions:
    print direct
#http://www.manjulaskitchen.com/2008/02/17/battura/
#http://www.manjulaskitchen.com/2007/04/01/dhokla-suji-semolina/
#http://www.manjulaskitchen.com/2008/03/10/punjabi-chola/
#http://www.manjulaskitchen.com/2015/04/02/tawa-naan-without-tandoor/
#pList = bsObj.findAll("p")
#iList = bsObj.findAll("ul")
#for div in divList:
#     print(div.get_text())    
#for p in pList:
#    print(p.get_text())
#for i in iList:
#    print(i.get_text())    #    
#filename = 'sample_manjulas_recipie.txt'
#with open(filename, 'w') as filetowrite:
#    filetowrite.write('\n'.join(ingreds))
