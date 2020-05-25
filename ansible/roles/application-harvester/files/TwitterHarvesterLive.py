"""
# Project           : Gig Economy and its impact in Australia
# Team              : Group 33
# City              : Melbourne, Australia
# Authors           : Qing Feng Chye 770376, Sii Kim Lau 890511, Rohan Jahagirdar 835450
#                     Yun Liu 1046589, Shorye Chopra 689913
# Purpose           : Twitter Harvester for live data
"""
import tweepy
import json
import couchdb_requests
from TwitterHarvesterFunc import mainFunction, getLocation, isRetweet, isUseful, extractTweetImpAttr


class MyStreamListener(tweepy.StreamListener):
    variables = {}

    def __init__(self, time_limit=60):
        self.limit = time_limit
        self.tweet_data = []
        with open('variables.json') as json_file:
            self.variables = json.load(json_file)

    def on_status(self, status):
        print(status.text)

    def on_error(self, status_code):
        if status_code == 420:
            #returning False in on_error disconnects the stream
            return True

    def on_data(self, data):
        extractedTweets = CheckTwitter(json.loads(data), self.variables["harvester_generic"]["keywords"], self.variables["harvester_generic"]["regions"])
        if extractedTweets != False:
            print("FINALLY FOUND A TWEET THAT IS USEFUL!")
            print(extractedTweets)
            couchdb_requests.couch_post(self.variables, extractedTweets)

def StartStream(keywords, language, variables):
   
    auth = tweepy.OAuthHandler(variables["harvester_live"]["tweepy_auth"]["auth_id"], variables["harvester_live"]["tweepy_auth"]["auth_key"])
    auth.set_access_token(variables["harvester_live"]["access_token"]["token_id"], variables["harvester_live"]["access_token"]["token_key"])
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=auth, listener=myStreamListener)
    myStream.filter(track=keywords, languages=language, is_async = True)

def CheckTwitter(tweet, all_keywords, region):
    loc = getLocation(tweet)
    try:
        text = tweet['text']
        if (loc in region) and (not isRetweet(text)):
            for keyword in all_keywords:
                if (isUseful(keyword, text)):
                    return extractTweetImpAttr(tweet, loc, keyword, text)
    except Exception:
        pass
        return False

    return False

def main():
    
    variables = {}
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    keywords = variables["harvester_generic"]["keywords"]
    language = ['en']
    StartStream(keywords, language, variables)

    return


main()

