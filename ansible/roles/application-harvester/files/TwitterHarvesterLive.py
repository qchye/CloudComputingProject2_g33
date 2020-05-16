import tweepy
import json
import couchdb_requests
from TwitterHarvesterFunc import mainFunction, all_keywords, all_regions, getLocation, isRetweet, isUseful, extractTweetImpAttr


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
        extractedTweets = CheckTwitter(json.loads(data), all_keywords, all_regions)
        if extractedTweets != False:
            print("FINALLY FOUND A TWEET THAT IS USEFUL!")
            print(extractedTweets)
            couchdb_requests.couch_post(self.variables, extractedTweets)

def StartStream(keywords, language, variables):
   
    auth = tweepy.OAuthHandler(variables["harvester_live"]["tweepy_auth"]["auth_id"], variables["harvester_live"]["tweepy_auth"]["auth_key"])
    auth.set_access_token("1252833883516624903-Ym6NDMEmTgaFhUK4dOcEHzsN4ZQfr6", "MIloYNYqgp6hwEREQBEEzri6DshW2UljsRhVdKxa5WiQM")
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

