from collections import defaultdict
import numpy as np
import matplotlib.pyplot as plt
import couchdb_requests
import os
import pandas as pd
# to account for matplotlib version <3.1
import matplotlib
matplotlib.use('Agg')


# plot the chart: stateGig
def GetLocalGig():
    response = couchdb_requests.couch_get_localGig({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                   "_design/LocalGig/",
                                                   "_view/local-gig-view",
                                                   "?reduce=true&group_level=1")
    statemap = defaultdict(int)
    for i in response["rows"]:
        print("State: %s" % i["key"][0] + " ,Count: %d" % i["value"])
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

    # print(statemap)
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


# plot the chart:The sentiment variable in all years
def Getsentiment():
    response = couchdb_requests.couch_get_unemployVSsentiment({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                              "twitter/_design/regionVSsentiment/",
                                                              "_view/senti",
                                                              "?reduce=true&group_level=1")
    statemap = defaultdict(int)
    for i in response["rows"]:
        location = i["key"][0]
        # calulate the sentiment value for each region.
        value = i["value"]['sum']/i["value"]['count']

        # group value by state
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
    ax.bar(statekeys, statevalues, width=0.5)
    ax.set_ylabel('Sentiment Rate')
    ax.set_title('Sentiment About Gig Economy')
    ax.set_xticklabels(statekeys)

    for a, b in zip(statekeys, statevalues):
        plt.text(a, b+0.01, round(b, 3), horizontalalignment='center',
                 verticalalignment='center')
    fig.savefig('img/sentiment.png')

    return 'img/sentiment.png'


# plot the chart:Unemployment in 2018
def Getunemploy():
    response = couchdb_requests.couch_get_unemployVSsentiment({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                              "aurin-employment-gcc/_design/states_unemploy/",
                                                              "_view/unemploy_rate",
                                                              "?reduce=true&group_level=3")

    unemployrate = defaultdict(float)
    for i in response["rows"]:
        location = i["key"][0]
        total = i["key"][1]+i["key"][2]+i['value']

        rate = i["value"]/total  # calulate the unemployment rate

        # group value by state
        if location == "New South Wales":
            unemployrate["NSW"] += round(rate, 4)
        elif location == "Queensland":
            unemployrate["QLD"] += round(rate, 4)
        elif location == "South Australia":
            unemployrate["SA"] += round(rate, 4)
        elif location == "Victoria":
            unemployrate["VIC"] += round(rate, 4)
        elif location == "Western Australia":
            unemployrate["WA"] += round(rate, 4)

    # start plot
    statekeys = list(unemployrate.keys())
    statevalues = list(unemployrate.values())
    fig, ax = plt.subplots()
    ax.barh(statekeys, statevalues, height=0.5)
    ax.set_xlabel('Unemployment Rate', fontsize=12)
    ax.set_ylabel('States in Australia', fontsize=12)
    ax.set_title('Unemployment Rate in 2018', fontsize=16)
    ax.set_yticklabels(statekeys)
    for a, b in zip(statevalues, statekeys):
        plt.text(a-0.003, b, '{:.2%}'.format(a),
                 horizontalalignment='center', verticalalignment='center')
    fig.savefig('img/unemployment_rate.png')
    return 'img/unemployment_rate.png', unemployrate


# plot the chart:The sentiment variable in 2018
def GetsentimentD():
    response = couchdb_requests.couch_get_unemployVSsentiment({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                              "twitter/_design/regionVSsentiment/",
                                                              "_view/senti_date",
                                                              "?reduce=true&group_level=2")
    count = defaultdict(int)
    statemap = defaultdict(int)
    for i in response["rows"]:
        location = i["key"][0]
        date = i["key"][1]
        year = date.split(' ')[-1]

        # find the data that in 2018
        if year == '2018':
            value = i["value"]['sum']

            if location == "Melbourne":
                count['VIC'] += 1
                statemap["VIC"] += value
            elif location == "Adelaide":
                count['SA'] += 1
                statemap["SA"] += value
            elif location == "Brisbane":
                count['QLD'] += 1
                statemap["QLD"] += value
            elif location == "Canberra":
                count['NSW'] += 1
                statemap["NSW"] += value
            elif location == "Darwin":
                count['NT'] += 1
                statemap["NT"] += value
            elif location == "Hobart":
                count['TAS'] += 1
                statemap["TAS"] += value
            elif location == "Perth":
                count['WA'] += 1
                statemap["WA"] += value
            elif location == "Sydney":
                count['NSW'] += 1
                statemap["NSW"] += value
            elif location == "Victoria":
                count['VIC'] += 1
                statemap["VIC"] += value
            elif location == "South Australia":
                count['SA'] += 1
                statemap["SA"] += value
            elif location == "Queensland":
                count['QLD'] += 1
                statemap["QLD"] += value
            elif location == "New South Wales":
                statemap["NSW"] += value
            elif location == "Northern Territory":
                count['NT'] += 1
                statemap["NT"] += value
            elif location == "Tasmania":
                count['TAS'] += 1
                statemap["TAS"] += value
            elif location == "Western Australia":
                count['WA'] += 1
                statemap["WA"] += value
            else:
                count[location] += 1
                statemap[location] += value
    # print(count)
    for key in statemap.keys():
        statemap[key] = statemap[key]/count[key]

    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())

    # start plot
    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues, width=0.5)
    ax.set_ylabel('Sentiment Rate', fontsize=12)
    ax.set_xlabel('States in Australia', fontsize=12)
    ax.set_title('Sentiment to Gig Economy in 2018', fontsize=16)
    ax.set_xticklabels(statekeys)

    for a, b in zip(statekeys, statevalues):
        plt.text(a, b+0.0025, round(b, 3),
                 horizontalalignment='center', verticalalignment='center')
    fig.savefig('img/sentiment2018.png')

    return 'img/sentiment2018.png', statemap


# plot the chart: the relation of sentiment VS unemployment
def CombinePlot():
    Getsentiment()
    y = []
    unemploy = Getunemploy()[1]
    senti = GetsentimentD()[1]
    x = list(unemploy.values())
    keys = list(unemploy.keys())

    # bulid a dataset for unemployment with sentiment
    for key in keys:
        y.append(senti[key])

     # start plot
    fig, ax = plt.subplots()
    ax.scatter(x, y, c='b', marker='o')
    plt.grid()
    ax.set_ylabel('Sentiment Rate', fontsize=12)
    ax.set_xlabel('Unemployment Rate', fontsize=12)
    ax.set_title('Relation Between Sentiment and Unemployment', fontsize=16)
    plt.grid(True)
    fig.savefig('img/comparing.png')
    return 'img/comparing.png'


def GetMedAgePopulation():
    response = couchdb_requests.couch_get_agePopulation({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                        "_design/population/",
                                                        "_view/population")
    statemap = defaultdict(int)
    freq = defaultdict(int)
    # going through the twitter data from couchdb
    # do data processing
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
    # get the avg
    for state, value in statemap.items():
        statemap[state] = round(value/freq[state], 1)
    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())
    # bar chart plotting
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


def GetElderlyPopPercentage():
    response = couchdb_requests.couch_get_agePopulation({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                        "_design/population/",
                                                        "_view/population")
    statemap = defaultdict(int)
    freq = defaultdict(int)
    # going through the twitter data from couchdb
    # do data processing
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
    # get the avg (after rounding to 2 decimal places)
    for state, value in statemap.items():
        statemap[state] = round(value/freq[state], 1)
    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())
    # bar chart plotting
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
# Initialise the state map with the states of Australia with zero value


def initialiseStateMap():
    state_keys = ['VIC', 'SA', 'QLD', 'NT', 'TAS', 'WA', 'NSW']
    statemap = {key: 0 for key in state_keys}
    return statemap
# check if the data is useless (all states have zero value)


def checkAllSentimentZero(statemap):
    length = 0
    for value in statemap.values():
        if (value == 0):
            length += 1
    return len(statemap) == length
# Get all the keywords with data


def GetUsefulKeywords():
    response = couchdb_requests.couch_get_localGig({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                   "_design/GigSentimental/",
                                                   "_view/sentimentOnStateKeywordYear",
                                                   "?reduce=true&group_level=3")
    usefulKeywords = []
    keywordsList = ['airbnb', 'airly', 'airtasker', 'bettercaring', 'camplify', 'carnextdoor', 'classbento', 'deliveroo', 'designcrowd', 'doordash', 'ebay', 'etsy', 'fiverr', 'gocatch', 'gumtree', 'helpling', 'homeaway',
                    'hometime', 'lyft', 'menulog', 'olacab', 'parkhound', 'pawshake', 'ratesetter', 'redbubble', 'shebah', 'sidekicker', 'spacer', 'stayz', 'stellar', 'taxify', 'uber', 'upwork', 'urbansitter', 'zomato', 'zoom2u']
    locList = ['Melbourne', 'Adelaide', 'Brisbane', 'Canberra', 'Darwin', 'Hobart', 'Perth', 'Sydney', 'Victoria',
               'South Australia', 'Queensland', 'New South Wales', 'Northern Territory', 'Tasmania', 'Western Australia']
    for i in response["rows"]:
        location = i["key"][0]
        word = i["key"][1]
        year = i["key"][2]
        # only want data for the particular keyword selected in 2017
        if (word in keywordsList and year == "2017"):
            if location in locList:
                # check if the keyword already exists in the list or not
                if (word not in usefulKeywords):
                    usefulKeywords.append(word)
    return usefulKeywords


def GetKeywordSentiment(keyword):
    response = couchdb_requests.couch_get_localGig({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                                                   "_design/GigSentimental/",
                                                   "_view/sentimentOnStateKeywordYear",
                                                   "?reduce=true&group_level=3")
    statemap = initialiseStateMap()
    freq = defaultdict(int)
    for i in response["rows"]:
        location = i["key"][0]
        word = i["key"][1]
        year = i["key"][2]
        # only want data for the particular keyword selected in 2017
        # data processing
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
    # get the avg (rounding to 2 decimal places)
    for state, value in statemap.items():
        if (freq[state] != 0):
            value = (value/freq[state] * 100)
            statemap[state] = round(value, 2)
    # store the state with the lowest sentiment value and the sentiment value
    (lowestSentState, lowestSentValue) = min((key, value)
                                             for key, value in statemap.items() if value is not 0)
    isHypothesisTrue = False
    # assume negative sentiment initially
    isTasNegative = True
    isSANegative = True
    # hypothesis true
    if (statemap["TAS"] < 0 and statemap["SA"] < 0):
        isHypothesisTrue = True
    # check if tasmania has positive sentiment
    if (statemap["TAS"] > 0):
        isTasNegative = False
    # check if south australia has positive sentiment
    if (statemap["SA"] > 0):
        isSANegative = False
    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())
    # bar chart plotting
    fig, ax = plt.subplots()
    # draw a line on y=0
    plt.axhline(y=0, linestyle='-', color='black')
    ax.bar(statekeys, statevalues, color='green')
    ax.set_ylabel('Sentiment (%)')
    ax.set_title('Sentiment Value on Gig Economy Based \n on \"' +
                 keyword + '\" keyword ' + 'for States of Australia', loc='center')
    ax.set_xticklabels(statekeys)
    for a, b in zip(statekeys, statevalues):
        if (b == 0):
            plt.text(a, b, "", horizontalalignment='center')
        elif (b < 0):
            plt.text(a, b - 1.7, str(b), horizontalalignment='center')
        else:
            plt.text(a, b + 0.4, str(b), horizontalalignment='center')
    fig.savefig('img/keywordSentiment.png')

    return ("img/keywordSentiment.png", isHypothesisTrue, isTasNegative, isSANegative, lowestSentState, lowestSentValue)
