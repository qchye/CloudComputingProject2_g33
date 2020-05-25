"""
# Project           : Gig Economy and its impact in Australia
# Team              : Group 33
# City              : Melbourne, Australia
# Authors           : Qing Feng Chye 770376, Sii Kim Lau 890511, Rohan Jahagirdar 835450
#                     Yun Liu 1046589, Shorye Chopra 689913
# Purpose           : Helper file for building fault-tolerant HTTP Request functions
"""
import requests
import http
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from requests.auth import HTTPBasicAuth
from requests_toolbelt.utils import dump

def requests_retry_session(
    retries=3,
    backoff_factor=1,
    status_forcelist=(500, 502, 504),
    method_whitelist=["HEAD", "GET", "PUT", "DELETE", "POST"],
    session=None,
    couch_vars={}
):
    """
    
    Function to ensure that there's fault tolerance when making API Calls to Couch 
    retries -> Total number of retries
    backoff_factor -> How long the processes will sleep between failed requests
        Calculation for it is = {backoff factor} * (2 ** ({number of total retries} - 1))
    status_forcelist -> The HTTP response codes to retry on
    session -> Deafult to create a new session otherwise use an existing
    method_whitelist -> The HTTP methods to retry on
    vars -> Variables dictionary
    """
    session = session or requests.Session()
    retry = Retry(
        total=retries,
        read=retries,
        connect=retries,
        backoff_factor=backoff_factor,
        status_forcelist=status_forcelist,
        method_whitelist=method_whitelist
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount('http://', adapter)
    # Uncomment line below to get logging on the request
    # session.hooks["response"] = [logging_hook]
    session.auth = (couch_vars['USERNAME'], couch_vars['PASSWORD'])
    return session

def logging_hook(response, *args, **kwargs):
    data = dump.dump_all(response)
    print(data.decode('utf-8'))

def couch_post(couch_vars ,tweet):
    print(tweet)
    try:
        s = requests.Session()
        response = requests_retry_session(session=s, couch_vars=couch_vars).post(couch_vars['COUCHDB_BASE_URL'] + "twitter", json = tweet)
        response.raise_for_status()

    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
           print("Bad Request was Sent")
           return False
        elif e.response.status_code == 409:
            print("Document exists in DB")
            return False
        else:
           print(e.__class__.__name__)
           return False
    except Exception as e: 
        print('Failure Caused by ', e.__class__.__name__)
        return False
    else:
        print(response.json())
        print('It eventually worked', response.status_code)
        return True
    

    