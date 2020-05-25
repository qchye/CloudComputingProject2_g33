import couchdb_requests
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

# The sentiment variable in all years
def Getsentiment():
    response = couchdb_requests.couch_get_unemployVSsentiment({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                      "twitter/_design/regionVSsentiment/",
                      "_view/senti",
                      "?reduce=true&group_level=1")
    statemap = defaultdict(int)
    for i in response["rows"]:
        location = i["key"][0]
        value =i["value"]['sum']/i["value"]['count'] # calulate the sentiment value for each region.

        #group value by state
        if location == "Melbourne":
            statemap["VIC"] +=value
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
    print(statevalues)
    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues,width=0.5)
    ax.set_ylabel('Sentiment Rate')
    ax.set_title('Sentiment About Gig Economy')
    ax.set_xticklabels(statekeys)

    for a,b in zip(statekeys, statevalues):
        plt.text(a, b+0.01, round(b,3),horizontalalignment='center',verticalalignment='center')
    fig.savefig('img/sentiment.png')
            
    return 'img/sentiment.png'

# Unemployment in 2018
def Getunemploy():
    response = couchdb_requests.couch_get_unemployVSsentiment({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                    "aurin-employment-gcc/_design/states_unemploy/",
                    "_view/unemploy_rate",
                    "?reduce=true&group_level=3")

    unemployrate=defaultdict(float)
    for i in response["rows"]:
        location = i["key"][0]
        total=i["key"][1]+i["key"][2]+i['value']

        rate =i["value"]/total # calulate the unemployment rate

        #group value by state
        if location == "New South Wales":
            unemployrate["NSW"] += round(rate,4)
        elif location == "Queensland":
            unemployrate["QLD"] += round(rate,4)
        elif location == "South Australia":
            unemployrate["SA"] += round(rate,4)
        elif location == "Victoria":
            unemployrate["VIC"] += round(rate,4)
        elif location == "Western Australia":
            unemployrate["WA"] += round(rate,4)  

    statekeys = list(unemployrate.keys())
    statevalues = list(unemployrate.values())
    fig, ax = plt.subplots()
    ax.barh(statekeys, statevalues, height=0.5)
    ax.set_xlabel('Unemployment Rate',fontsize=12)
    ax.set_ylabel('States in Australia',fontsize=12)
    ax.set_title('Unemployment Rate in 2018',fontsize=16)
    ax.set_yticklabels(statekeys)
    for a,b in zip(statevalues,statekeys ):
        plt.text(a-0.003, b, '{:.2%}'.format(a),horizontalalignment='center',verticalalignment='center')
    fig.savefig('img/unemployment_rate.png')
    return 'img/unemployment_rate.png',unemployrate

# plot the chart:The sentiment variable in 2018
def GetsentimentD():
    response = couchdb_requests.couch_get_unemployVSsentiment({"COUCHDB_BASE_URL": "http://172.26.133.111:8080/", "USERNAME": "admin", "PASSWORD": "admin"},
                      "twitter/_design/regionVSsentiment/",
                      "_view/senti_date",
                      "?reduce=true&group_level=2")
    count=defaultdict(int)
    statemap = defaultdict(int)
    for i in response["rows"]:
        location = i["key"][0]
        date=i["key"][1]
        year=date.split(' ')[-1]

        #find the data that in 2018
        if year == '2018':
            value =i["value"]['sum']

            if location == "Melbourne":
                count['VIC']+=1
                statemap["VIC"] +=value
            elif location == "Adelaide":
                count['SA']+=1
                statemap["SA"] += value
            elif location == "Brisbane":
                count['QLD']+=1
                statemap["QLD"] += value
            elif location == "Canberra":
                count['NSW']+=1
                statemap["NSW"] += value
            elif location == "Darwin":
                count['NT']+=1
                statemap["NT"] += value
            elif location == "Hobart":
                count['TAS']+=1
                statemap["TAS"] += value
            elif location == "Perth":
                count['WA']+=1
                statemap["WA"] += value
            elif location == "Sydney":
                count['NSW']+=1
                statemap["NSW"] += value
            elif location == "Victoria":
                count['VIC']+=1
                statemap["VIC"] += value
            elif location == "South Australia":
                count['SA']+=1
                statemap["SA"] += value 
            elif location == "Queensland":
                count['QLD']+=1
                statemap["QLD"] += value
            elif location == "New South Wales":
                statemap["NSW"] += value
            elif location == "Northern Territory":
                count['NT']+=1
                statemap["NT"] += value
            elif location == "Tasmania":
                count['TAS']+=1
                statemap["TAS"] += value
            elif location == "Western Australia":
                count['WA']+=1
                statemap["WA"] += value
            else:
                count[location]+=1
                statemap[location] += value
    #print(count)
    for key in statemap.keys():
        statemap[key]=statemap[key]/count[key]
   
    statekeys = list(statemap.keys())
    statevalues = list(statemap.values())
    
    fig, ax = plt.subplots()
    ax.bar(statekeys, statevalues,width=0.5)
    ax.set_ylabel('Sentiment Rate',fontsize=12)
    ax.set_xlabel('States in Australia',fontsize=12)
    ax.set_title('Sentiment to Gig Economy in 2018',fontsize=16)
    ax.set_xticklabels(statekeys)

    for a,b in zip(statekeys, statevalues):
        plt.text(a, b+0.0025, round(b,3),horizontalalignment='center',verticalalignment='center')
    fig.savefig('img/sentiment2018.png')
            
    return 'img/sentiment2018.png',statemap

# plot the chart: the relation of sentiment VS unemployment
def CombinePlot():
    Getsentiment()
    y=[]
    unemploy=Getunemploy()[1]
    senti=GetsentimentD()[1]
    x = list(unemploy.values())
    keys= list(unemploy.keys())

    for key in keys:
        y.append(senti[key])
    
    fig, ax = plt.subplots()
    ax.scatter(x, y,c='b',marker='o')
    plt.grid()
    ax.set_ylabel('Sentiment Rate',fontsize=12)
    ax.set_xlabel('Unemployment Rate',fontsize=12)
    ax.set_title('Relation Between Sentiment and Unemployment',fontsize=16)
    plt.grid(True)
    fig.savefig('img/comparing.png')        
    return 'img/comparing.png'
    
CombinePlot()
