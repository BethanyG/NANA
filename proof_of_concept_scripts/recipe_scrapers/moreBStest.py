# -*- coding: utf-8 -*-
"""
Created on Thu Aug  6 13:44:17 2015

@author: bethanygarcia
"""

from urllib2 import urlopen 
from bs4 import BeautifulSoup
html = urlopen("http://www.pythonscraping.com/pages/page3.html") 
bsObj = BeautifulSoup(html, "lxml") 
print(bsObj.find("img",{"src":"../img/gifts/img1.jpg"}).parent.previous_sibling.get_text())