"""
# Project           : Gig Economy and its impact in Australia
# Team              : Group 33
# City              : Melbourne, Australia
# Authors           : Qing Feng Chye 770376, Sii Kim Lau 890511, Rohan Jahagirdar 835450
#                     Yun Liu 1046589, Shorye Chopra 689913
# Purpose           : Manual Twitter Harvester for Uploading data manally to couchdb
"""
from TwitterHarvesterFunc import all_keywords,all_regions,CheckFriendsTwitter
import json
import couchdb_requests

def manualHarvesttxt():
    inputfile='./tweetsGigRes.txt'
    variables = {}
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    for line in open(inputfile,encoding='utf-8'):
        try:
            tweets=json.loads(line)
        except:
            pass
        #print(CheckFriendsTwitter(tweets, all_keywords, all_regions))
        single_result = CheckFriendsTwitter(tweets, all_keywords, all_regions)
        if single_result != False:
            couchdb_requests.couch_post(variables, single_result)
    return


def manualHarvestMel():
    inputfile='./twitter-melb.json'
    tweet=''
    single_result=False
    variables = {}
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    for line in open(inputfile,encoding='utf-8'):       
        try:
            tweets=json.loads(line[:-2])
            tweet=tweets['doc']
            single_result = CheckFriendsTwitter(tweet, all_keywords, all_regions)
            
        except:
            pass
        
        if single_result != False:
            couchdb_requests.couch_post(variables, single_result)
    return
##
# Function to add the income data to CouchDB
##

def manualHarvestPop(inputfile):
    
    variables = {}
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    
    with open(inputfile) as f:
        data = json.load(f)

        features = data['features']
        #Custom keys to make column names legible
        for row in features:
            doc = {'_id': row['id']}
            for key in row['properties']:
                
                if (key == 'est_res_pop_ur_erp_30_jun_med_age_ur_erp_30_jun_f_yrs'):
                    doc['med_female_years'] = row['properties'][key]

                elif (key == 'est_res_pop_ur_erp_30_jun_med_age_ur_erp_30_jun_m_yrs'):
                    doc['med_male_years'] = row['properties'][key]

                elif (key == 'est_res_pop_ur_erp_30_jun_p_tot_num'):
                    doc['med_june_male_years'] = row['properties'][key]
                
                elif (key == 'est_res_pop_ur_erp_30_jun_p_wrking_age_pop_15_64_yrs_pr100'):
                    doc['working_age_pop_pr100'] = row['properties'][key]
                
                elif (key == 'est_res_pop_ur_erp_30_jun_f_tot_num'):
                    doc['female_pop_total'] = row['properties'][key]
                
                elif (key == 'est_res_pop_ur_erp_30_jun_m_tot_num'):
                    doc['male_pop_total'] = row['properties'][key]
                
                elif (key == 'est_res_pop_ur_erp_30_jun_med_age_ur_erp_30_jun_p_yrs'):
                    doc['med_years'] = row['properties'][key]

                else:
                    doc[key] = row['properties'][key]

            print(doc)
            couchdb_requests.couch_post_other(variables, doc, "aurin-population")

##
# Function to upload aurin data into couchdb for analysis
##
def manualHarvestMisc(inputfile, dbname):
    variables = {}
    with open('variables.json') as json_file:
        variables = json.load(json_file)
    
    #Open file
    with open(inputfile) as f:
        data = json.load(f)
    #use the existing json keys as keys for storing in database
        features = data['features']
        for row in features:
            doc = {'_id': row['id']}
            for key in row['properties']:
                doc[key] = row['properties'][key]

            print(doc)
            couchdb_requests.couch_post_other(variables, doc, dbname)


manualHarvesttxt()
manualHarvestMel() 
manualHarvestPop('../../../../datasets/ABS_-_Data_by_Region_-_Population___People__GCCSA__2011-2018.json/data7100197488286421467.json')
manualHarvestMisc('../../../../datasets/DJSB_Small_Area_Labour_Market_-_Unemployment_SA2_2010-2018.json/data3617067625698803929.json', "aurin-employment-sa2")
manualHarvestMisc('../../../../datasets/Employment_Rate_State_2018/Employment_json/data8173168136821074606.json', "aurin-employment-gcc")
manualHarvestMisc('../../../../datasets/GCCSA_Estimates_of_Personal_Income_-_Employee_Income_by_Occupation_and_Sex_2010-2015.json/data7633999421168806682.json', "aurin-mean-income")


  
   
    
    
    
    
    
    
    