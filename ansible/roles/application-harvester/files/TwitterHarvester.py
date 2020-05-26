"""
# Project           : Gig Economy and its impact in Australia
# Team              : Group 33
# City              : Melbourne, Australia
# Authors           : Qing Feng Chye 770376, Sii Kim Lau 890511, Rohan Jahagirdar 835450
#                     Yun Liu 1046589, Shorye Chopra 689913
# Purpose           : Twitter Harvester main entrypoint
"""
import tweepy
import json
from TwitterHarvesterFunc import mainFunction


def main():
    
    variables = {}
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    auth = tweepy.AppAuthHandler(
        variables["harvester_historic"]["tweepy_auth"]["auth_id"], variables["harvester_historic"]["tweepy_auth"]["auth_key"])
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    half_keywords = variables["harvester_historic"]["keywords_processed"]
    keywords = variables["harvester_generic"]["keywords"]
    region = variables["harvester_generic"]["regions"]
    count = variables["harvester_generic"]["max_count"]
    language = 'en'
    mainFunction(api, half_keywords, keywords, count, language, region, variables)
    return


main()
