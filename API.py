import requests
import json

def get_azure_pricing():
    url = 'https://prices.azure.com/api/retail/prices'
    response = requests.get(url)
    return response.json()

def get_aws_pricing():
    url = 'https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/20230713195841/us-west-2-den-1/index.json'
    response = requests.get(url)
    return response.json()
    

def get_gcp_pricing():
    url = 'https://cloudpricingcalculator.appspot.com/static/data/pricelist.json'
    response = requests.get(url)
    return response.json()

azure_pricing = get_azure_pricing()
aws_pricing = get_aws_pricing()
gcp_pricing = get_gcp_pricing()

pricing_data = {
    'Azure': azure_pricing,
    'AWS': aws_pricing,
    'GCP': gcp_pricing
}

json_data = json.dumps(pricing_data, indent=4)
print(json_data)
