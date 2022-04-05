import requests
import json
import os
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv('rainforest_key')

def GetAvailabilityJSON(_asin):
    params = {
      'api_key': 'demo',
      'type': 'stock_estimation',
      'amazon_domain': 'amazon.com',
      'asin': _asin,
      'output': 'json'
    }

    # make the http GET request to Rainforest API
    api_result = requests.get('https://api.rainforestapi.com/request', params)
    response = api_result.json()

    #print(response["stock_estimation"]["stock_level"])
    #print(response["stock_estimation"]["availability_message"])
    #print(response["stock_estimation"]["price"]["value"])
    return(response)

#answer = GetAvailabilityJSON('B073JYC4XM')

#print("The price is:",answer["stock_estimation"]["price"]["value"])
