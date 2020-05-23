import couchdb_requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

def GetLocalGig():
    response = couchdb_requests.couch_get_localGig({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                      "_design/LocalGig/",
                      "_view/local-gig-view",
                      "?reduce=true&group_level=1")
    statemap = defaultdict(int)
    for i in response["rows"]:
        print("State: %s"%i["key"][0] + " ,Count: %d"%i["value"])
        location = i["key"][0]
        value = i["value"]

        if location == "Melbourne":
            statemap["VIC"] += value
        elif location == "Adelaide":
            statemap["SA"] += value
        elif location == "Brisbane":
            statemap["QLD"] += value
        elif location == "Canberra":
            statemap["NSW"] += value
        elif location == "Darwin":
            statemap["NT"] += value
        elif location == "Hobart":
            statemap["TAS"] += value
        elif location == "Perth":
            statemap["WA"] += value
        elif location == "Sydney":
            statemap["NSW"] += value
        elif location == "Victoria":
            statemap["VIC"] += value
        elif location == "South Australia":
            statemap["SA"] += value
        elif location == "Queensland":
            statemap["QLD"] += value
        elif location == "New South Wales":
            statemap["NSW"] += value
        elif location == "Northern Territory":
            statemap["NT"] += value
        elif location == "Tasmania":
            statemap["TAS"] += value
        elif location == "Western Australia":
            statemap["WA"] += value
        else:
            statemap[location] += value

    #print(statemap)
    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())
    response = couchdb_requests.couch_get_localGig({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                      "_design/LocalGig/",
                      "_view/local-gig-view",
                     "?reduce=true&group_level=2")

    for i in response["rows"]:
       print("State: %s"%i["key"][0] + " ,Keyword: %s"%i["key"][1] + " ,Count: %d"%i["value"])
    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues)
    ax.set_ylabel('Count')
    ax.set_title('Num of Gig economy was tweeted in states in Australia')
    ax.set_xticklabels(statekeys)
    for a,b in zip(statekeys, statevalues):
        plt.text(a, b, str(b))
    fig.savefig('img/stateGig.png')
    return "img/stateGig.png"
GetLocalGig()