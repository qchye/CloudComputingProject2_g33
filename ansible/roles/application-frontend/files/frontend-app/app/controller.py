from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import couchdb_requests
import os
import pandas as pd
# to account for matplotlib version <3.1
import matplotlib
matplotlib.use('Agg')


def GetLocalGig():
    response = couchdb_requests.couch_get_localGig({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                   "_design/LocalGig/",
                                                   "_view/local-gig-view",
                                                   "?reduce=true&group_level=1")
    statemap = defaultdict(int)
    for i in response["rows"]:
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

    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())
    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues)
    ax.set_ylabel('Count')
    ax.set_title(
        'Num of Gig economy was tweeted in states of Australia from 2010 to 2020')
    ax.set_xticklabels(statekeys)
    for a, b in zip(statekeys, statevalues):
        plt.text(a, b + 130, str(b), horizontalalignment='center',
                 verticalalignment='center')
    fig.savefig('img/stateGig.png')
    return "img/stateGig.png"


def GetMedAgePopulation():
    response = couchdb_requests.couch_get_agePopulation({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                        "_design/population/",
                                                        "_view/population")
    statemap = defaultdict(int)
    freq = defaultdict(int)

    for i in response["rows"]:
        location = i["key"]
        value = i["value"]["med_year"]

        if location == "Greater Melbourne":
            statemap["VIC"] += value
            freq["VIC"] += 1
        elif location == "Greater Adelaide":
            statemap["SA"] += value
            freq["SA"] += 1
        elif location == "Greater Brisbane":
            statemap["QLD"] += value
            freq["QLD"] += 1
        elif location == "Greater Darwin":
            statemap["NT"] += value
            freq["NT"] += 1
        elif location == "Greater Hobart":
            statemap["TAS"] += value
            freq["TAS"] += 1
        elif location == "Greater Perth":
            statemap["WA"] += value
            freq["WA"] += 1
        elif location == "Greater Sydney":
            statemap["NSW"] += value
            freq["NSW"] += 1
        elif location == "Rest of Vic.":
            statemap["VIC"] += value
            freq["VIC"] += 1
        elif location == "Rest of SA":
            statemap["SA"] += value
            freq["SA"] += 1
        elif location == "Rest of Qld":
            statemap["QLD"] += value
            freq["QLD"] += 1
        elif location == "Rest of NSW":
            statemap["NSW"] += value
            freq["NSW"] += 1
        elif location == "Rest of NT":
            statemap["NT"] += value
            freq["NT"] += 1
        elif location == "Rest of Tas.":
            statemap["TAS"] += value
            freq["TAS"] += 1
        elif location == "Rest of WA":
            statemap["WA"] += value
            freq["WA"] += 1
        else:
            statemap[location] += value
            freq[location] += 1

    for state, value in statemap.items():
        statemap[state] = round(value/freq[state], 1)

    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())

    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues, color='red')
    ax.set_ylabel('Age')
    ax.set_title('Median Age for States of Australia in 2017')
    ax.set_xticklabels(statekeys)
    for a, b in zip(statekeys, statevalues):
        plt.text(a, b + 0.6, str(b), horizontalalignment='center',
                 verticalalignment='center')
    fig.savefig('img/medianAge.png')
    return "img/medianAge.png"


def GetWAPopPercentage():
    response = couchdb_requests.couch_get_agePopulation({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                        "_design/population/",
                                                        "_view/population")
    statemap = defaultdict(int)
    freq = defaultdict(int)

    for i in response["rows"]:
        location = i["key"]
        value = i["value"]["working_age_pop_pr100"]

        if location == "Greater Melbourne":
            statemap["VIC"] += value
            freq["VIC"] += 1
        elif location == "Greater Adelaide":
            statemap["SA"] += value
            freq["SA"] += 1
        elif location == "Greater Brisbane":
            statemap["QLD"] += value
            freq["QLD"] += 1
        elif location == "Greater Darwin":
            statemap["NT"] += value
            freq["NT"] += 1
        elif location == "Greater Hobart":
            statemap["TAS"] += value
            freq["TAS"] += 1
        elif location == "Greater Perth":
            statemap["WA"] += value
            freq["WA"] += 1
        elif location == "Greater Sydney":
            statemap["NSW"] += value
            freq["NSW"] += 1
        elif location == "Rest of Vic.":
            statemap["VIC"] += value
            freq["VIC"] += 1
        elif location == "Rest of SA":
            statemap["SA"] += value
            freq["SA"] += 1
        elif location == "Rest of Qld":
            statemap["QLD"] += value
            freq["QLD"] += 1
        elif location == "Rest of NSW":
            statemap["NSW"] += value
            freq["NSW"] += 1
        elif location == "Rest of NT":
            statemap["NT"] += value
            freq["NT"] += 1
        elif location == "Rest of Tas.":
            statemap["TAS"] += value
            freq["TAS"] += 1
        elif location == "Rest of WA":
            statemap["WA"] += value
            freq["WA"] += 1
        else:
            statemap[location] += value
            freq[location] += 1

    for state, value in statemap.items():
        statemap[state] = round(value/freq[state], 1)

    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())

    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues, color='magenta')
    ax.set_ylabel('Population (%)')
    ax.set_title('Working Age Population for States of Australia in 2017')
    ax.set_xticklabels(statekeys)
    for a, b in zip(statekeys, statevalues):
        plt.text(a, b + 1, str(b), horizontalalignment='center',
                 verticalalignment='center')
    fig.savefig('img/workingAgePop.png')
    return "img/workingAgePop.png"


def GetElderlyPopPercentage():
    response = couchdb_requests.couch_get_agePopulation({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                        "_design/population/",
                                                        "_view/population")
    statemap = defaultdict(int)
    freq = defaultdict(int)

    for i in response["rows"]:
        location = i["key"]
        value = i["value"]["elderly_pop_pr100"]

        if location == "Greater Melbourne":
            statemap["VIC"] += value
            freq["VIC"] += 1
        elif location == "Greater Adelaide":
            statemap["SA"] += value
            freq["SA"] += 1
        elif location == "Greater Brisbane":
            statemap["QLD"] += value
            freq["QLD"] += 1
        elif location == "Greater Darwin":
            statemap["NT"] += value
            freq["NT"] += 1
        elif location == "Greater Hobart":
            statemap["TAS"] += value
            freq["TAS"] += 1
        elif location == "Greater Perth":
            statemap["WA"] += value
            freq["WA"] += 1
        elif location == "Greater Sydney":
            statemap["NSW"] += value
            freq["NSW"] += 1
        elif location == "Rest of Vic.":
            statemap["VIC"] += value
            freq["VIC"] += 1
        elif location == "Rest of SA":
            statemap["SA"] += value
            freq["SA"] += 1
        elif location == "Rest of Qld":
            statemap["QLD"] += value
            freq["QLD"] += 1
        elif location == "Rest of NSW":
            statemap["NSW"] += value
            freq["NSW"] += 1
        elif location == "Rest of NT":
            statemap["NT"] += value
            freq["NT"] += 1
        elif location == "Rest of Tas.":
            statemap["TAS"] += value
            freq["TAS"] += 1
        elif location == "Rest of WA":
            statemap["WA"] += value
            freq["WA"] += 1
        else:
            statemap[location] += value
            freq[location] += 1

    for state, value in statemap.items():
        statemap[state] = round(value/freq[state], 1)

    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())

    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues, color='blue')
    ax.set_ylabel('Population (%)')
    ax.set_title('Elderly Population for States of Australia in 2017')
    ax.set_xticklabels(statekeys)
    for a, b in zip(statekeys, statevalues):
        plt.text(a, b + 0.5, str(b), horizontalalignment='center',
                 verticalalignment='center')
    fig.savefig('img/elderlyAgePop.png')
    return "img/elderlyAgePop.png"


def GetKeywordSentiment(keyword):
    response = couchdb_requests.couch_get_localGig({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                   "_design/GigSentimental/",
                                                   "_view/sentimentOnStateKeywordYear",
                                                   "?reduce=true&group_level=3")
    statemap = defaultdict(int)
    freq = defaultdict(int)

    for i in response["rows"]:
        location = i["key"][0]
        word = i["key"][1]
        year = i["key"][2]

        # only want data for the particular keyword selected in 2017
        if (word == keyword and year == "2017"):

            value = i["value"]

            if location == "Melbourne":
                statemap["VIC"] += value
                freq["VIC"] += 1
            elif location == "Adelaide":
                statemap["SA"] += value
                freq["SA"] += 1
            elif location == "Brisbane":
                statemap["QLD"] += value
                freq["QLD"] += 1
            elif location == "Canberra":
                statemap["NSW"] += value
                freq["NSW"] += 1
            elif location == "Darwin":
                statemap["NT"] += value
                freq["NT"] += 1
            elif location == "Hobart":
                statemap["TAS"] += value
                freq["TAS"] += 1
            elif location == "Perth":
                statemap["WA"] += value
                freq["WA"] += 1
            elif location == "Sydney":
                statemap["NSW"] += value
                freq["NSW"] += 1
                print(statemap["NSW"])
            elif location == "Victoria":
                statemap["VIC"] += value
                freq["VIC"] += 1
            elif location == "South Australia":
                statemap["SA"] += value
                freq["SA"] += 1
            elif location == "Queensland":
                statemap["QLD"] += value
                freq["QLD"] += 1
            elif location == "New South Wales":
                statemap["NSW"] += value
                freq["NSW"] += 1
                print(statemap["NSW"])
            elif location == "Northern Territory":
                statemap["NT"] += value
                freq["NT"] += 1
            elif location == "Tasmania":
                statemap["TAS"] += value
                freq["TAS"] += 1
            elif location == "Western Australia":
                statemap["WA"] += value
                freq["WA"] += 1
            else:
                statemap[location] += value
                freq[location] += 1

    for state, value in statemap.items():
        statemap[state] = round(value/freq[state], 2)
        print("State: %s" % state + ", Count: %d" %
              value + ", year = %s" % year)

    print(statemap)
    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())

    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues, color='green')
    ax.set_ylabel('Sentiment (%)')
    ax.set_title('Sentiment Value on Gig Economy Based on \"' +
                 keyword + '\" keyword ' + 'for States of Australia', loc='center')
    ax.set_xticklabels(statekeys)
    for a, b in zip(statekeys, statevalues):
        plt.text(a, b, str(b), horizontalalignment='center',
                 verticalalignment='center')
    fig.savefig('img/keywordSentiment.png')
    return "img/keywordSentiment.png"
