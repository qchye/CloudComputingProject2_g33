# -*- coding: utf-8 -*-
"""
Created on Sun May  3 12:59:23 2020

@author: yun liu
"""
from re import search

#filter tweets: only the one match both region and keywords will be returned
def ProcessTwitter(tweet,keywords,region):
    text=tweet['text']
    place=tweet['place']
    if len(place) != 0:
        loc=place['country_code']
    else:
        user=tweet['user']
        location=user['location']
        loc=location.split(',')[0]
    for w in keywords:
        if search(w.lower(), text.lower()) and loc in region:
            tweet
            break
    return

def main():
    tweet=[]
    keywords=['park','breaking']
    region=['AU','Melbourne','Sydney','Quensland','Australia','Western Australia','South Australia','Victoria']
    ProcessTwitter(tweet,keywords,region)
    return

main()