import couchdb_requests
import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
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

    print(statemap)
    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                      "_design/LocalGig/",
                      "_view/local-gig-view",
                     "?reduce=true&group_level=2")


    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues)
    ax.set_ylabel('Count')
    ax.set_title('Num of Gig economy was tweeted in states in Australia')
    ax.set_xticklabels(statekeys)
    for a,b in zip(statekeys, statevalues):
        plt.text(a, b, str(b))
    fig.savefig('img/stateGig.png')
    return "img/stateGig.png"
#GetLocalGig()

def get_income_tweet():
    variables = {}
    variables = load_variables()

    # Get the Aurin Income Data
    response = couchdb_requests.couch_get_view(variables, "aurin-mean-income/",
                      "_design/city-income/",
                      "_view/gccsavsincome-view/", "")


    city_income_dict = {}
    
    for row in response["rows"]:
        city_income_dict[row["key"]] = row["value"]
    
    city_income_dict = state_sorter_aurin(city_income_dict)
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/location-keyword/",
                    "_view/locationvskeyword/", "?reduce=true&group_level=1")    
    city_count_dict = {}
    for row in response["rows"]:
        city_count_dict[row["key"][0]] = row["value"] 

    city_count_dict = state_sorter_twitter(city_count_dict)
    # city_count_dict.pop('OT')


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
    
    fig.savefig('img/incomevstweets.png')
    return "img/incomevstweets.png"

get_income_tweet()



def get_unemployment_tweet():
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables, "aurin-employment-sa2/",
                    "_design/unemployment_doc/",
                    "_view/sa2_vs_decdata/", "?reduce=true&group_level=1")

    unemployment_count = {}
    for row in response["rows"]:
        unemployment_count[row["key"]] = row["value"]

    unemployment_count['QLD'] =  [4348, 4386, 4950, 4528, 5129, 5872, 5941, 5664]
    total = []
   

    #get tweets
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/location-keyword/",
                    "_view/year_keyword/", "?reduce=true&group_level=1")
    
    year_count = {}
    for row in response["rows"]:
        year_count[row["key"][0]] = row["value"]

    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/location-keyword/",
                    "_view/year_location/", "?reduce=true&group_level=2")
    year_location_count = {}
    for key in unemployment_count.keys():
        year_location_count[key] = {}
    for row in response["rows"]: 
        year_location_count[row["key"][1]].update({row["key"][0]:row["value"]})

    #create graph one unemployment vs year per state
    x_axis = ['2010','2011','2012','2013','2014','2015','2016','2017']
    plt_1 = plt.figure(1,figsize=(8,8))
    for state in unemployment_count.keys():
        plt.plot(x_axis, unemployment_count[state], label = state)
    
    plt.xlabel('year', fontsize=16)
    plt.ylabel('no. of people unemployed', fontsize=16)
    plt.title('Unemployment vs Year (State)', fontsize=20)
    plt_1.legend()
    plt_1.savefig('img/unemp_vs_year_state.png')
    
    #create graph two unemployment vs year overall
    total = np.zeros(len(unemployment_count['VIC']))
    for value in unemployment_count.values():
        for i in range(len(value)):
            total[i] += value[i]

    plt_2 = plt.figure(2, figsize=(8,8))
    plt.plot(x_axis, total)
    plt.xlabel('year', fontsize=16)
    plt.ylabel('no. of people unemployed', fontsize=16)
    plt.title('Unemployment vs Year', fontsize=20)
    plt_2.savefig('img/unemp_vs_year.png')
    x_axis_4 = list(year_count.keys())
    y_axis_4 = []
    
    for year in x_axis:
        y_axis_4.append(year_count[year])
    
    plt_3 = plt.figure(3, figsize=(8,8))
    plt.plot(x_axis, y_axis_4)
    plt.xlabel('year', fontsize=16)
    plt.ylabel('no. of gig economy tweets', fontsize=16)
    plt.title('Gig Economy Tweets vs year', fontsize=20)
    plt_3.savefig('img/tweets_vs_year_state.png')

    images = ['img/unemp_vs_year_state.png', 'img/unemp_vs_year.png', 'img/tweets_vs_year_state.png']
    return images
get_unemployment_tweet()


def get_business_popularity():
    #twitter data keyword count
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/keyword_count/",
                    "_view/keyword_popular/", "?reduce=true&group_level=1")
    keyword_count_dict = {}
    for row in response["rows"]:
        keyword_count_dict[row["key"]] = row["value"]
    y_pos = list(keyword_count_dict.keys())
    x_pos = list(keyword_count_dict.values())
    plt.rcdefaults()
    fig, ax = plt.subplots(figsize=(10,10))
    y_arrange = np.arange(len(y_pos))
    ax.barh(y_arrange, x_pos, align='center')
    ax.set_yticks(y_arrange)
    ax.set_yticklabels(y_pos)
    ax.invert_yaxis()  # labels read top-to-bottom
    ax.set_xlabel('Number of Tweets')
    ax.set_title('Popularity of Gig Economy Businesses')
    
    fig.savefig('img/keyword_pop.png')
    return "img/keyword_pop.png"

get_business_popularity()

def get_business_pop_location():
    #keyword count per location
    variables = {}
    variables = load_variables()
    response = couchdb_requests.couch_get_view(variables, "twitter/",
                    "_design/location-keyword/",
                    "_view/locationvskeyword/", "?reduce=true&group_level=2")
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
    #create graph
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
        fig.savefig('img/keyword_loc_'+state+'.png')
        images.append('img/keyword_loc_'+state+'.png')
    return images
get_business_pop_location()