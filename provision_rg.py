from azure.mgmt.resource import ResourceManagementClient
from azure.identity import AzureCliCredential

credential = AzureCliCredential()
subscription_id = "603f1137-266a-461d-beac-a4d2984f9dc1"
client = ResourceManagementClient(credential, subscription_id)

resource_grp = client.resource_groups.create_or_update("Migration", {"location": "southindia"})

print(f"Privison the resource group {resource_grp.name}")