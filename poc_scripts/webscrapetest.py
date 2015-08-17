# -*- coding: utf-8 -*-
"""
Created on Wed Aug  5 12:40:11 2015

@author: bethanygarcia
"""

from urllib import urlopen
from urllib2 import HTTPError
from bs4 import BeautifulSoup

def getTitle(url): 
    try:
        html = urlopen(url) 
    except HTTPError as e:
        return None 
    
    try:
        bsObj = BeautifulSoup(html.read(), "lxml")
        title = bsObj.body.h1 
    except AttributeError as e:
        return None 
    return title

title = getTitle("http://www.manjulaskitchen.com/2015/04/02/tawa-naan-without-tandoor/") 
if title == None:
    print("Title could not be found") 
else:
    print(title)