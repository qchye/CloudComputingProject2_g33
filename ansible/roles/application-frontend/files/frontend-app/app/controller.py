"""
# Project           : Gig Economy and its impact in Australia
# Team              : Group 33
# City              : Melbourne, Australia
# Authors           : Qing Feng Chye 770376, Sii Kim Lau 890511, Rohan Jahagirdar 835450
#                     Yun Liu 1046589, Shorye Chopra 689913
# Purpose           : Controller File for the frontend MVC Flask application
"""
from collections import defaultdict
import matplotlib.pyplot as plt
import couchdb_requests
import os
import pandas as pd
import numpy as np
from collections import defaultdict
import json


''' Helper functions for the data gathering '''
def load_variables():
    variables = {}
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    
    return variables

def state_sorter_twitter(states_dict):
    statemap = defaultdict(int)

    for location in states_dict.keys():
        if location == "Melbourne":
            statemap["VIC"] += states_dict[location]
        elif location == "Adelaide":
            statemap["SA"] += states_dict[location]
        elif location == "Brisbane":
            statemap["QLD"] += states_dict[location]
        elif location == "Canberra":
            statemap["ACT"] += states_dict[location]
        elif location == "Darwin":
            statemap["NT"] += states_dict[location]
        elif location == "Hobart":
            statemap["TAS"] += states_dict[location]
        elif location == "Perth":
            statemap["WA"] += states_dict[location]
        elif location == "Sydney":
            statemap["NSW"] += states_dict[location]
        elif location == "Victoria":
            statemap["VIC"] += states_dict[location]
        elif location == "South Australia":
            statemap["SA"] += states_dict[location]
        elif location == "Queensland":
            statemap["QLD"] += states_dict[location]
        elif location == "New South Wales":
            statemap["NSW"] += states_dict[location]
        elif location == "Northern Territory":
            statemap["NT"] += states_dict[location]
        elif location == "Tasmania":
            statemap["TAS"] += states_dict[location]
        elif location == "Western Australia":
            statemap["WA"] += states_dict[location]
        else:
            statemap[location] += states_dict[location]

    return statemap


#helper function to sort data into states for aurin gccsa
def state_sorter_aurin(states_dict):
    new_state_dict = defaultdict(int)
    for key in states_dict.keys():

        if key == 'Australian Capital Territory':
            new_state_dict['ACT'] += states_dict[key]

        elif key == 'Greater Adelaide':
            new_state_dict['SA'] += states_dict[key]

        elif key == 'Greater Brisbane':
            new_state_dict['QLD'] += states_dict[key]
        
        elif key == 'Greater Darwin':
            new_state_dict['NT'] += states_dict[key]

        elif key == 'Greater Hobart':
            new_state_dict['TAS'] += states_dict[key]

        elif key == 'Greater Melbourne':
            new_state_dict['VIC'] += states_dict[key]

        elif key == 'Greater Sydney':
            new_state_dict['NSW'] += states_dict[key]

        elif key == 'Greater Perth':
            new_state_dict['WA'] += states_dict[key]

        elif key == 'Rest of NSW':
            new_state_dict['NSW'] += states_dict[key]

        elif key == 'Rest of NT':
            new_state_dict['NT'] += states_dict[key]

        elif key == 'Rest of Qld':
            new_state_dict['QLD'] += states_dict[key]

        elif key == 'Rest of SA':
            new_state_dict['SA'] += states_dict[key]
        
        elif key == 'Rest of Tas.':
            new_state_dict['TAS'] += states_dict[key]

        elif key == 'Rest of Vic.':
            new_state_dict['VIC'] += states_dict[key]

        elif key == 'Rest of WA':
            new_state_dict['WA'] += states_dict[key]

        else:
            pass
    
    for key in new_state_dict.keys():
        if key != 'ACT':
            new_state_dict[key] = new_state_dict[key]/2
        
    return new_state_dict




'''Controller functions for processing of couchdb data'''


def GetLocalGig():
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                      "_design/LocalGig/",
                      "_view/local-gig-view",
                      "?reduce=true&group_level=1")
    statemap = {}
    for row in response["rows"]:
        statemap[row["key"][0]] = row["value"]

    statemap = state_sorter_twitter(statemap)

    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                      "_design/LocalGig/",
                      "_view/local-gig-view",
                     "?reduce=true&group_level=2")

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
#GetLocalGig()


# plot the chart:The sentiment variable in all years
def Getsentiment():
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables,
                                                              "twitter/", "_design/regionVSsentiment/",
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
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables,
                                                              "aurin-employment-gcc/", "_design/states_unemploy/",
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
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables,
                                                              "twitter/", "_design/regionVSsentiment/",
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
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables, "aurin-population/",
                                                        "_design/population/",
                                                        "_view/population/", "")
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
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables,"aurin-population/",
                                                        "_design/population/",
                                                        "_view/population/","")
    statemap = defaultdict(int)
    freq = defaultdict(int)
    # going through the twitter data from couchdb
    # do data processing
    print(response)
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
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                                                   "_design/GigSentimental/",
                                                   "_view/sentimentOnStateKeywordYear",
                                                   "?reduce=true&group_level=3")
    usefulKeywords = []
    keywordsList = ['airbnb', 'airly', 'airtasker', 'bettercaring', 'camplify', 'carnextdoor', 'classbento', 'deliveroo', 'designcrowd', 'doordash', 'ebay', 'etsy', 'fiverr', 'gocatch', 'gumtree', 'helpling', 'homeaway',
                    'lyft', 'menulog', 'olacab', 'parkhound', 'pawshake', 'ratesetter', 'redbubble', 'shebah', 'sidekicker', 'spacer', 'stayz', 'stellar', 'uber', 'upwork', 'urbansitter', 'zomato', 'zoom2u']
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
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables, "twitter/",
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
    (lowestSentValue, lowestSentState) = min((value, key)
                                             for key, value in statemap.items() if value != 0)
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


'''
# Function to get views from Twitter database about the location of tweets 
# as well as the mean income across Australia and compare the two
#
# @returns: Image file path and saves graph image to /img folder
'''
def get_income_tweet():
    variables = {}
    variables = load_variables()

    # Get the Aurin Income Data
    response = couchdb_requests.couch_get_view(variables, "aurin-mean-income/",
                      "_design/city-income/",
                      "_view/gccsavsincome-view/", "")

    #Parse the response
    city_income_dict = {}
    
    for row in response["rows"]:
        city_income_dict[row["key"]] = row["value"]
    
    #Get the twitter data for that location
    city_income_dict = state_sorter_aurin(city_income_dict)
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/location-keyword/",
                    "_view/locationvskeyword/", "?reduce=true&group_level=1")    
    #Parse the response
    city_count_dict = {}
    for row in response["rows"]:
        city_count_dict[row["key"][0]] = row["value"] 

    city_count_dict = state_sorter_twitter(city_count_dict)


    # create graph
    incomes = list(city_income_dict.values())
    tweet_num = list(city_count_dict.values())
    states = list(city_count_dict.keys())
    fig, ax = plt.subplots()
    ax.scatter(incomes, tweet_num)
    ax.set_xlabel('Mean Income ($)')
    ax.set_ylabel('Number of Tweets')
    for i in range(len(incomes)):
        ax.annotate(' ' + states[i], (incomes[i], tweet_num[i]), )
    
    #save and return image
    fig.savefig('img/incomevstweets.png')
    return "img/incomevstweets.png"

get_income_tweet()



def get_unemployment_tweet():
    variables = {}
    variables = load_variables()
    #get unemployment data from view
    response = couchdb_requests.couch_get_view(variables, "aurin-employment-sa2/",
                    "_design/unemployment_doc/",
                    "_view/sa2_decdata/", "?reduce=true&group_level=1")
    #parse the response
    unemployment_count = {}
    for row in response["rows"]:
        unemployment_count[row["key"]] = row["value"]

    unemployment_count['QLD'] =  [4348, 4386, 4950, 4528, 5129, 5872, 5941, 5664]
    total = []
   

    #get tweets based on year
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/location-keyword/",
                    "_view/year_keyword/", "?reduce=true&group_level=1")
    
    #parse response for graphing
    year_count = {}
    for row in response["rows"]:
        year_count[row["key"][0]] = row["value"]

    #get tweets based on location
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/location-keyword/",
                    "_view/year_location/", "?reduce=true&group_level=2")
    year_location_count = {}
    for key in unemployment_count.keys():
        year_location_count[key] = {}
    for row in response["rows"]: 
        year_location_count[row["key"][1]].update({row["key"][0]:row["value"]})

    #create graph one: unemployment vs year per state
    x_axis = ['2010','2011','2012','2013','2014','2015','2016','2017']
    plt_1 = plt.figure(1,figsize=(10,10))
    for state in unemployment_count.keys():
        plt.plot(x_axis, unemployment_count[state], label = state)
    
    plt.xlabel('year', fontsize=14)
    plt.ylabel('no. of people unemployed', fontsize=14)
    plt.title('Unemployment vs Year (State)', fontsize=20)
    plt_1.legend(loc=7)
    plt_1.savefig('img/unemp_vs_year_state.png')
    
    #create graph two: unemployment vs year overall
    total = np.zeros(len(unemployment_count['VIC']))
    for value in unemployment_count.values():
        for i in range(len(value)):
            total[i] += value[i]

    plt_2 = plt.figure(2, figsize=(8,8))
    plt.plot(x_axis, total)
    plt.xlabel('year', fontsize=14)
    plt.ylabel('no. of people unemployed', fontsize=14)
    plt.title('Unemployment vs Year', fontsize=20)
    plt_2.savefig('img/unemp_vs_year.png')

    #create graph two: unemployment vs year overall
    x_axis_4 = list(year_count.keys())
    y_axis_4 = []
    
    for year in x_axis:
        y_axis_4.append(year_count[year])
    
    plt_3 = plt.figure(3, figsize=(8,8))
    plt.plot(x_axis, y_axis_4, color="red")
    plt.xlabel('year', fontsize=16)
    plt.ylabel('no. of gig economy tweets', fontsize=16)
    plt.title('Gig Economy Tweets vs year', fontsize=20)
    plt_3.savefig('img/tweets_vs_year_state.png')

    #save and return images
    images = ['img/unemp_vs_year_state.png', 'img/unemp_vs_year.png', 'img/tweets_vs_year_state.png']
    return images
get_unemployment_tweet()

'''
# Function to get views from Twitter database about the tweet counts of various keywords
# @returns: Image file path and saves graph image to /img folder
'''

def get_business_popularity():
    
    variables = {}
    variables = load_variables()
    # Extract popular keyword view
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/keyword_count/",
                    "_view/keyword_popular/", "?reduce=true&group_level=1")
    

    #store response in dictionary
    keyword_count_dict = {}
    for row in response["rows"]:
        keyword_count_dict[row["key"]] = row["value"]
    y_pos = list(keyword_count_dict.keys())
    x_pos = list(keyword_count_dict.values())

    #plot the graph
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(10,10))
    y_arrange = np.arange(len(y_pos))
    ax.barh(y_arrange, x_pos, align='center', color="red")
    ax.set_yticks(y_arrange)
    ax.set_yticklabels(y_pos)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of Tweets')
    ax.set_title('Popularity of Gig Economy Businesses')

    #save and return image path
    fig.savefig('img/keyword_pop.png')
    return "img/keyword_pop.png"

'''
# Function to get views from Twitter database about the tweet counts of various keywords
# @returns: Image file path array for each state and saves graph images to /img folder
'''
def get_business_pop_location():
    
    variables = {}
    variables = load_variables()

    # Extract popular keyword view
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/location-keyword/",
                    "_view/locationvskeyword/", "?reduce=true&group_level=2")

    # Parse the response and store popularity according to each state
    states = ['VIC', 'NSW', 'WA', 'SA', 'NT', 'ACT', 'QLD', 'TAS']                
    keyword_loc_dict = {}
    for key in states:
        keyword_loc_dict[key] = {}
    for row in response["rows"]:
        if (row["key"][0] == 'OT'):
            pass
        else:
            keyword_loc_dict[row["key"][0]].update({row["key"][1]:row["value"]})

    images = []
    #create graph for each state
    for state in states:
        y_pos = list(keyword_loc_dict[state].keys())
        x_pos = list(keyword_loc_dict[state].values())
        plt.rcdefaults()
        fig, ax = plt.subplots(figsize=(10,10))
        y_arrange = np.arange(len(y_pos))
        ax.barh(y_arrange, x_pos, align='center')
        ax.set_yticks(y_arrange)
        ax.set_yticklabels(y_pos)
        ax.invert_yaxis()  # labels read top-to-bottom
        ax.set_xlabel('Number of Tweets')
        ax.set_title('Popularity of Gig Economy Businesses in ' + state)
        #save figure for state
        fig.savefig('img/keyword_loc_'+state+'.png')
        images.append('img/keyword_loc_'+state+'.png')
    return images