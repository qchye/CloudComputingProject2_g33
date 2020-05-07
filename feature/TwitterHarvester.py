import tweepy
import json

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
            print(tweet_json)
            # We only interested the tweets in Australia and keyword in text
            if CheckTwitterLocation(tweet_json, region):
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

# filter tweets: only the one match region


def CheckTwitterLocation(tweet, region):
    useful = False
    text = tweet['text']
    place = tweet['place']
    if place != None:
        loc = place['country_code']
    else:
        user = tweet['user']
        location = user['location']
        loc = location.split(',')[0]

    if (loc in region):
        print("found xD")
        useful = True

    return useful

# As going into friend's list, need to check all keywords


def CheckFriendsTwitter(tweet, query, region):
    useful = False
    text = tweet['text']
    place = tweet['place']
    if place != None:
        loc = place['country_code']
    else:
        user = tweet['user']
        location = user['location']
        loc = location.split(',')[0]

    if (loc in region):
        for w in query:
            if w.lower() in text.lower():
                print("found & Current Keyword = %s" % w.lower())
                useful = True

    return useful


def main():

    auth = tweepy.AppAuthHandler(
        "X7zGj3Ow4bPu05Em8WGGsko3G", "VkYgRxRkid5Ru4cpU7QineZIK2icnpRIHpZpVGaH8RlSYCJIQG")
    api = tweepy.API(auth, wait_on_rate_limit=True,
                     wait_on_rate_limit_notify=True)
    keywords = ['airbnb', 'stayz', 'zomato', 'deliveroo', 'hungrypanda',
                'lyft', 'olacab', '#grab', 'grabcar', 'didirider', 'menulog',
                'taxify', 'etsy', 'gumtree', 'fiverr', 'cookitoo', 'uber',
                'expedia', 'airtasker', 'freelancer', 'parkhound', 'campspace',
                'upwork', 'designcrowd', 'ratesetter', 'urbansitter', 'airly',
                'gocatch', 'shebah', 'bellhops', 'channel40', 'freightmatch',
                'wrappli', 'zoom2u', 'carnextdoor', 'camplify', 'kindershare',
                'quipmo', 'thevolte', 'bettercaring', '#blys', 'classbento',
                'helpling']
    region = ['AU', 'Melbourne', 'Sydney', 'Queensland', 'Australia',
              'Western Australia', 'South Australia', 'Victoria']
    count = 10000
    language = 'en'
    mainFunction(api, keywords, count, language, region)

    return


main()

# Stream API goes here


class MyStreamListener(tweepy.StreamListener):

    def __init__(self, time_limit=60):
        self.limit = time_limit
        self.tweet_data = []

    def on_status(self, status):
        print(status.text)

    def on_data(self, data):
        print(data)


def StartStream(keywordList, language):
    myStreamListener = MyStreamListener()
    myStream = tweepy.Stream(auth=auth1, listener=myStreamListener)
    myStream.filter(track=keywordList, languages=language)
