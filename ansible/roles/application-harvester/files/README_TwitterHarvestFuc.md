# Twitter Harvester

## Imported Packages
In order to do get all the required information to the CouchDB, the 7 packages: 'tweepy', 'json', 're','TextBlob','nltk', 'ssl' and 'SentimentIntensityAnalyzer' are used. 
'tweepy': for curl the tweets from Tweeter
'json': read the 'json' file
're': using the regular expression for find the useful tweets.
'TextBlob': Breakup the text to sentences.
'nltk': Installing  'Punkt' from it.
'ssl': Handle the errors when download 'Punkt' from nltk.
'SentimentIntensityAnalyzer': soring the sentiment for each sentence.

## mainFunction(api, query, count, language, region)
Using tweet.Cursor find the most resent tweets and using 'searchFriends' to find historical tweets for the tweets' friends, check the query and region for those tweets, return the useful one.
### Inputs
aqi:The 'api' for getting the tweets from Twitter
query: a words-list which will be used to filter the tweets.
count: The number of tweets harvest for each request.
language: 'en'
region:a list of region which we will consider for analysis.}

## searchFriends(api, target)
Get a list of follower's ids for the target account, 
### Input
target: user id who post a tweet resently, 
api: a URL for getting tweets.
### Output 
A list of friend's ID. 

## ProcessRelatedTweets(api, friendsIdList, query, region, totalExplored, totalUsefulTweets):
This function is for finding all the tweets in the required timeline for all the user in friends list, and then filter out the tweets that do not contain the query and not in the given region.
### Output:{
The total number of tweets that in the timeline and the tweets that matches all the conditions.

## CheckTwitterLocation(tweet, region)
This function is for checking whether the current tweets in the defined region for filter the user.
### Output:
Boolean: True or False.


## CheckFriendsTwitter(tweet, query, region)
This function is for check whether the friends's tweets is useful or not.The 'tweet' which gets from the friends post, will be tested whether the tweet in the defined region and contains the keyword in query or not.
### Output:
Boolean: True or False.

## extractTweetImpAttr(tweet, loc, keyword, text)
This function is to build a dictionary for stroing the key information which will be used in CouchDB.The dictionary contains 6 attributes: 'id' the tweets id; 'created_at': the time of the tweet created; 'text': the tweet; 'location': the location of the user or the place of the tweet posted; 'ketword': the keyword that the tweet contains; 'sentimental': the sore of the writer's sentiment in this tweet.the sore is in [-1,1].
### OutPut:
 reqTweetAttr: a dictionary contian 6 attibutes for a single tweet.

## isUsful(keyword,text)
This function id for check whether the keyword is in the text or not.
### Output
Boolean: True or False.

## main() 
This function includes the authortication,api,keyword and regions information for the getting the useful tweets.(This function is in the TwitterHarvest2.py)

## Reference
1. textblob - https://textblob.readthedocs.io/en/dev/install.html

2. vaderSentiment - https://pypi.org/project/vaderSentiment/ 

Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.

3. NLTK package - https://www.nltk.org/install.html

4. 'Punkt' error handle: https://stackoverflow.com/questions/38916452/nltk-download-ssl-certificate-verify-failed


### Common out
'couchdb_requests',
'couchdb_requests': conncting to the couchDB for upload the database.
Upload the useful dictionary to CouchDB
