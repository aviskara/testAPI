import requests
import json

# set up the request parameters
params = {
  'api_key': 'demo',
  'type': 'stock_estimation',
  'amazon_domain': 'amazon.com',
  'asin': 'B073JYC4XM',
  'output': 'json'
}

# make the http GET request to Rainforest API
#api_result = requests.get('https://api.rainforestapi.com/request', params)

#with open("response.json", 'w') as json_file:
#  json.dump(api_result.json(), json_file)
#api_result.raise_for_status()
# print the JSON response from Rainforest API
f = open('response.json')
api_result = json.load(f)

response = api_result
print(response["stock_estimation"]["stock_level"])
print(response["stock_estimation"]["availability_message"])
print(response["stock_estimation"]["price"]["value"])