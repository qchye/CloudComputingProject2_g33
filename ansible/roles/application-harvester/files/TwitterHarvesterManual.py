
from TwitterHarvesterFunc import all_keywords,all_regions,CheckFriendsTwitter
import json
import couchdb_requests

def manualHarvesttxt():
    inputfile='./tweetsGigRes.txt'
    
    for line in open(inputfile,encoding='utf-8'):
        try:
            tweets=json.loads(line)
        except:
            pass
        #print(CheckFriendsTwitter(tweets, all_keywords, all_regions))
        single_result = CheckFriendsTwitter(tweets, all_keywords, all_regions)
        if single_result != False:
            couchdb_requests.couch_post(single_result)
    return


def manualHarvestMel():
    inputfile='./twitter-melb.json'
    tweet=''
    single_result=False
    
    for line in open(inputfile,encoding='utf-8'):       
        try:
            tweets=json.loads(line[:-2])
            tweet=tweets['doc']
            single_result = CheckFriendsTwitter(tweet, all_keywords, all_regions)
            
        except:
            pass
        
        if single_result != False:
            couchdb_requests.couch_post(single_result)
    return

manualHarvesttxt()
manualHarvestMel() 


  
   
    
    
    
    
    
    
    