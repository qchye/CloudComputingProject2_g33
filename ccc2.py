# -*- coding: utf-8 -*-
"""
Created on Sun May  3 12:59:23 2020

@author: yun liu
"""

import json
from re import search

#remove the attributes that are null
def cleanTweets(text):
    for key, value in list(text.items()):
        if value is None:
             del text[key]
        elif isinstance(value, dict):
            cleanTweets(value)
    return text

#filter tweets: only the one match both region and keywords will be returned
def ProcessTwitter(inputFile,keywords,region):
    Needed=[]
    for line in open(inputFile,encoding='utf-8'):
        tweets=json.loads(line)
        status=tweets['statuses']
        for term in status:
            tweet=dict(term)
            text=tweet['text']
            user=tweet['user']
            location=user['location']
            loc=location.split(',')[0]
            for w in keywords:
                if search(w.lower(), text.lower()) and loc in region:
                    ntweet=cleanTweets(tweet)
                    Needed.append(ntweet)   
    #dict={}; dict['need']=Needed
    return Needed

def main():
    inputFile ='./test.json'
    keywords=['park','breaking']
    region=['Melbourne','Sydney','Quensland','Australia','Western Australia','South Australia','Victoria']
    ProcessTwitter(inputFile,keywords,region)
    return

main()