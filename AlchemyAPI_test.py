# -*- coding: utf-8 -*-
"""
Created on Sat Aug 15 14:36:13 2015

@author: bethanygarcia
"""
from __future__ import print_function
from alchemyapi import AlchemyAPI
import json

alchemyapi = AlchemyAPI()

demo_text = '4 toasted slabs of whole grain bread, rubbed with olive oil and a bit of garlic'

#response = alchemyapi.sentiment("text", myText)
#print ("Sentiment: ", response["docSentiment"]["type"])

response = alchemyapi.combined('text', demo_text)

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')

    print('## Keywords ##')
    for keyword in response['keywords']:
        print(keyword['text'], ' : ', keyword['relevance'])
    print('')

    print('## Concepts ##')
    for concept in response['concepts']:
        print(concept['text'], ' : ', concept['relevance'])
    print('')

    print('## Entities ##')
    for entity in response['entities']:
        print(entity['type'], ' : ', entity['text'], ', ', entity['relevance'])
    print(' ')

else:
    print('Error in combined call: ', response['statusInfo'])
#http://access.alchemyapi.com/
#https://access.alchemyapi.com/