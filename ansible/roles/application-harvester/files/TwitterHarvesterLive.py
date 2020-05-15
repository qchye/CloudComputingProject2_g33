import tweepy
import json
import couchdb_requests
from TwitterHarvesterFunc import mainFunction, all_keywords, all_regions, getLocation, isRetweet, isUseful, extractTweetImpAttr

class MyStreamListener(tweepy.StreamListener):

    def __init__(self, time_limit=60):
        self.limit = time_limit
        self.tweet_data = []

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        extractedTweets = CheckTwitter(json.loads(data), all_keywords, all_regions)
        if extractedTweets != False:
            print("FINALLY FOUND A TWEET THAT IS USEFUL!")
            print(extractedTweets)
            couchdb_requests.couch_post(extractedTweets)

def StartStream(keywords, language):
   
    auth = tweepy.OAuthHandler("7K0xu6SgVlnA7nJwNVVPZHgSD", "MHIEp3ibXDKkVSilriKdRFFduvJn55ow6zsYdcU710wyui1Nil")
    auth.set_access_token("1252833883516624903-Ym6NDMEmTgaFhUK4dOcEHzsN4ZQfr6", "MIloYNYqgp6hwEREQBEEzri6DshW2UljsRhVdKxa5WiQM")
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=auth, listener=myStreamListener)
    myStream.filter(track=keywords, languages=language)

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

    keywords = all_keywords
    language = ['en']
    StartStream(keywords, language)

    return


main()

