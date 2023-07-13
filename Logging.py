import requests
import json

# Azure credentials
tenant_id = '<your-tenant-id>'
client_id = '<your-client-id>'
client_secret = '<your-client-secret>'
subscription_id = '<your-subscription-id>'
workspace_id = '<your-log-analytics-workspace-id>'

# Resource and log details
resource_group_name = '<your-resource-group-name>'
resource_name = '<your-resource-name>'
log_query = '<your-log-query>'

# Get an access token using a service principal
token_url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
data = {
    'grant_type': 'client_credentials',
    'client_id': client_id,
    'client_secret': client_secret,
    'resource': 'https://management.azure.com/'
}
response = requests.post(token_url, data=data)
access_token = response.json()['access_token']

# Query logs using the Log Analytics API
query_url = f"https://api.loganalytics.io/v1/workspaces/{workspace_id}/query"
headers = {
    'Authorization': f'Bearer {access_token}',
    'Content-Type': 'application/json'
}
query_payload = {
    'query': log_query,
    'timespan': '2023-07-01T00:00:00Z/2023-07-14T23:59:59Z'
}
response = requests.post(query_url, headers=headers, json=query_payload)

# Print the log query results
if response.status_code == 200:
    result = response.json()
    if 'tables' in result:
        for table in result['tables']:
            for row in table['rows']:
                print(row)
    else:
        print("No logs found.")
else:
    print("Log query failed. Status code:", response.status_code)