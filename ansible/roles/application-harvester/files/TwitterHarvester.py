import tweepy
import json
import re
import couchdb_requests


# Tweepy
# SEARCH API
# Search result based on query given, giving tweets, check tweets condition
def mainFunction(api, query, count, language, region):

    totalExplored = 0
    totalUsefulTweets = 0
    for keyword in query:
        print("Key word currently being searched: %s" % keyword)
        for tweet in tweepy.Cursor(api.search, q=[keyword], count=count, lang=language).items():

            tweet_json = tweet._json
            totalExplored += 1
            # We only interested the tweets in Australia and keyword in text
            if CheckTwitter(tweet_json, keyword, region):
                totalUsefulTweets += 1
                # Tweets storing process here, waiting for CouchDb

                print("==================================FINDING FRIENDS OF USER STARTS=============================================================================")
                # Finding Friends of friends section
                user = tweet_json['user']
                user_id = user['id']
                friendsIdList = searchFriends(api, user_id)
                totalExplored, totalUsefulTweets = ProcessRelatedTweets(
                    api, friendsIdList, query, region, totalExplored, totalUsefulTweets)

            print("Total Explored: %d" % totalExplored)
            print("Total Useful Tweets: %d" % totalUsefulTweets)

    return


# Get a list of follower ids for the target account, input take in user id, output friend's ID as a list
def searchFriends(api, target):

    friendsIDList = api.friends_ids(target, cursor=-1)[0]

    return friendsIDList


# Finding friends' timeline tweets, also check if the tweets is useful, and record accordingly
def ProcessRelatedTweets(api, friendsIdList, query, region, totalExplored, totalUsefulTweets):

    for Id in friendsIdList:

        try:
            # Searching tweets from timeline of user
            for tweet in tweepy.Cursor(api.user_timeline, id=Id).items():
                totalExplored += 1
                tweet_json = tweet._json
                # print(tweet_json)
                if CheckFriendsTwitter(tweet_json, query, region):
                    totalUsefulTweets += 1
                print("Total Explored: %d" % totalExplored)
                print("Total Useful Tweets: %d" % totalUsefulTweets)
        except Exception:  # Might because the user is private, so need to catch the exception.
            pass

    return (totalExplored, totalUsefulTweets)


# filter tweets: only the one match region with the keyword
def CheckTwitter(tweet, keyword, region):
    loc = getLocation(tweet)

    if (loc in region):
        if (isUseful(keyword, tweet['text'])):
            print("keyword found = %s" % keyword)
            print("tweet text = %s" % tweet['text'])
            return True

    return False


# As going into friend's list, need to check all keywords
def CheckFriendsTwitter(tweet, query, region):
    loc = getLocation(tweet)

    if (loc in region):
        for keyword in query:
            if (isUseful(keyword, tweet['text'])):
                print("keyword found = %s" % keyword)
                print("tweet text = %s" % tweet['text'])
                return True

    return False


def getLocation(tweet):
    place = tweet['place']
    if place != None:
        loc = place['country_code']
    else:
        user = tweet['user']
        location = user['location']
        loc = location.split(',')[0]

    return loc


def isUseful(keyword, text):
    if (re.search(r'\b{}'.format(keyword), text, flags=re.IGNORECASE)):
        return True

    return False


def main():

    auth = tweepy.AppAuthHandler(
        "X7zGj3Ow4bPu05Em8WGGsko3G", "VkYgRxRkid5Ru4cpU7QineZIK2icnpRIHpZpVGaH8RlSYCJIQG")
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    keywords = ['airbnb', 'stayz', 'zomato', 'deliveroo', 'hungrypanda',
                'lyft', 'olacab', '#grab', 'grabcar', 'didirider', 'menulog',
                'taxify', 'etsy', 'gumtree', 'fiverr', 'cookitoo', 'uber',
                'airtasker', '#freelancer', 'parkhound', 'campspace',
                'upwork', 'designcrowd', 'ratesetter', 'urbansitter', 'airly',
                'gocatch', 'shebah', 'bellhops', 'channel40', 'freightmatch',
                'wrappli', 'zoom2u', 'carnextdoor', 'camplify', 'kindershare',
                'quipmo', 'thevolte', 'bettercaring', '#blys', 'classbento',
                'helpling']
    region = ['AU', 'Melbourne', 'Sydney', 'Queensland', 'Australia',
              'Western Australia', 'South Australia', 'Victoria']
    count = 10000
    language = 'en'
    variables = {}
    mainFunction(api, keywords, count, language, region)
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    couchdb_requests.couchdb_test(variables)
    return


main()
