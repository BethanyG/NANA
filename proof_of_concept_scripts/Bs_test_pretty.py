# -*- coding: utf-8 -*-
"""
Created on Fri Sep 25 18:41:25 2015

@author: bethanygarcia
"""

from __future__ import print_function, division
import requests
from bs4 import BeautifulSoup, NavigableString, Tag, Comment
import nltk
import pattern
import re

#test_file = '/Users/bethanygarcia/.virtualenvs/Flask_project/Crap_html.html'

#with open (test_file, 'r') as raw:
#    html_text = raw.read()
#    bsObj = BeautifulSoup(html_text, 'html5lib')

raw= requests.get('http://www.hyperboleandahalf.blogspot.com/')
html_text = raw.text
bsObj = BeautifulSoup(html_text, 'html5lib')


print({tag.name : len(bsObj.find_all(tag.name)) for tag in bsObj.find_all(True)})
print("\n")
#print(tag.name for tag in bsObj.find_all())

#print(html_text)
#print(html_text)

#re_match = re.compile("</[^>]+>")
#re_match = re.compile("</[^>]+>")

#pattern_end = re.compile(r'</[a-z]+?[0-9]*>')
pattern_end = re.compile(r'</\w*>')

pattern_all = re.compile(r'</[^<]+[^<]+\w*\/*>|<[^<>]+[^<>]+\w*/*>')

#r'(</\W*\w*>)|(<\W*\w*>)

#pattern_begin = re.compile(r'<[a-z]+?[0-9]*>')
pattern_begin = re.compile(r'<\w*>')

#void_list = [area, base, br, col, command, embed, hr, img, input, keygen, link, meta, param, source, track, wbr]
pattern_void_tags = re.compile(r'<area|base|br|col|command|embed|hr|img|input|keygen|link|meta|param|source|track|wbr\s(\w*=*\"*\w*[\"-=:]*\"*)+>')

#pattern_lookbehind = re.compile('((?<=\<)\w*)|((?<=\<\/)\w*)')

#test_lookbehind = pattern_lookbehind.findall(html_text)
test_end = pattern_end.findall(html_text)
test_start = pattern_begin.findall(html_text)
test_all = pattern_all.findall(html_text)
test_void = pattern_void_tags.split(html_text)

tags_dict={}

for item in test_all:
    tags_dict.setdefault(item, 0)
    tags_dict[item] += 1
#words.setdefault('porcupine', []).append("hello")



#print(tags_dict)

#print(test_end)
#print("\n")
#print(test_start)
#print("\n")
#print(test_void)
#print("\n")
print(test_all)
print("\n")
#print(test_lookbehind)
#print("\n")
print(tags_dict)
print("\n")
#test = re.match("<?", html_text)

#print(test)

#bsObj = BeautifulSoup(html.content, 'html5lib')

#html_tags = {child.name : len(bsObj.find_all(child.name)) for child in bsObj.descendants if child.name is not None}
#html_tags_2 = {tag.name : tag for tag in bsObj.find_all(True, recurse=False)}


#tag_list=[]
#for tag in bsObj.find_all(True, recurse=False):
#    tag_list.append(tag.name)

#print(tag_list)
#test = bsObj.findAll(re.compile("</[^>]+>"))
#print(test)

#results_list=[]
#search_term = re.compile("</[^>]+>")



'''
import html.parser

class Parser(html.parser.HTMLParser):
    count = 0
    def handle_endtag(self, tag):
        if tag == 'html':
            self.count += 1

parser = Parser()
parser.feed('<html></html><!-- </html> --></html>')
parser.close()
print(parser.count)
'''