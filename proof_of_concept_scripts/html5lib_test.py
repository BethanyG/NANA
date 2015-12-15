# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 14:10:50 2015

@author: bethanygarcia
"""

import html5lib
from HTMLParser import HTMLParser
#import requests
import nltk
import pattern
import re
import urllib


>>> 'file:' + urllib.pathname2url(r'c:\path\to\something')
'file:///C:/path/to/something'




html = requests.get('http://www.example.com')
parser = html5lib.HTMLParser()
document = parser.parse(html.content)
 
tag_match = re.compile("<[^>]*[^/]>/g")

results = tag_match.match(document)

print results 