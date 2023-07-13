from azure.common.credentials import ServicePrincipalCredentials
from azure.mgmt.monitor import MonitorManagementClient

# Azure credentials
tenant_id = '<your-tenant-id>'
client_id = '<your-client-id>'
client_secret = '<your-client-secret>'
subscription_id = '<your-subscription-id>'

# Resource and metric details
resource_group_name = '<your-resource-group-name>'
resource_name = '<your-resource-name>'
metric_name = '<your-metric-name>'

# Authenticate using a service principal
credentials = ServicePrincipalCredentials(
    client_id=client_id,
    secret=client_secret,
    tenant=tenant_id
)

# Create the Azure Monitor client
monitor_client = MonitorManagementClient(credentials, subscription_id)

# Query the metric
metric_data = monitor_client.metrics.list(
    resource_group_name,
    resource_name,
    timespan='2023-07-01T00:00:00Z/2023-07-14T23:59:59Z',
    metricnames=metric_name,
    interval='PT1H'
)

# Print the metric values
for item in metric_data.value:
    print(item.name.localized_value)
    for timeseries in item.timeseries:
        for data in timeseries.data:
            print(data.time_stamp, data.total)