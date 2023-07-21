import requests
import pymongo
import json

def get_aws_price(location):
    url = "https://pricing.us-east-1.amazonaws.com/savingsPlan/v1.0/aws/AWSComputeSavingsPlan/current/region_index.json?region->regionCode="
    aws_response = requests.get(url)
    region_list = aws_response.json()

    #parsing json 
    matching_region = None
    for region in region_list['regions']:
        if region['regionCode'] == location:
            matching_region = region
            break

    if matching_region:
        version_url = matching_region['versionUrl']
        aws_data = requests.get(f'https://pricing.us-east-1.amazonaws.com{version_url}')
        data_list = aws_data.json()["terms"]["savingsPlan"]
        return data_list
    else:
        print(f"Data for location '{location}' not found.")
        return None 

def get_azure_price(num_of_items):
    url = "https://prices.azure.com/api/retail/prices?$filter=serviceName eq 'Virtual Machines' and serviceFamily eq 'Compute'"
    all_data = []
    skip_value = 0
    page_size = 100

    response = requests.get(url)
    data = response.json()
    items = data.get('Items', [])
    all_data.extend(items)

    while skip_value < num_of_items:
        url = f"https://prices.azure.com:443/api/retail/prices?$filter=serviceName%20eq%20%27Virtual%20Machines%27%20and%20serviceFamily%20eq%20%27Compute%27&$skip={skip_value}"
        response = requests.get(url)
        data = response.json()

        items = data.get('Items', [])
        all_data.extend(items)

        # Check if the response is empty (no more data to retrieve)
        if not data:
            break

        skip_value += page_size

    return all_data

def get_gcp_prices(api_key):
    base_url = "https://cloudbilling.googleapis.com/v1/services"
    params = {
        "key": api_key,
        "pageSize": 5000  
    }

    all_services = []
    next_page_token = None

    while True:
        if next_page_token:
            params["pageToken"] = next_page_token

        response = requests.get(base_url, params=params)
        data = response.json()

        if "services" in data:
            all_services.extend(data["services"])

        next_page_token = data.get("nextPageToken")
        if not next_page_token:
            break

    return all_services


client = pymongo.MongoClient("mongodb://localhost:27017/")

db = client["Cloud_API_Database"]

aws_collection = db["AWS EC2 Instances Pricing"]
azure_collection = db["Azure Compute VM Pricing"]
gcp_collection = db["Google Cloud Platform Services Pricing"]

aws_insert_result = aws_collection.insert_many(get_aws_price("us-east-1-scl-1"))
azure_insert_result = azure_collection.insert_many(get_azure_price(400))
gcp_insert_result = gcp_collection.insert_many(get_gcp_prices("AIzaSyBAKm03OFL9sQlPUFH8xm5V1vCKccURiqo"))






