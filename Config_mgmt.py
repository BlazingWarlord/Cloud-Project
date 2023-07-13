from azure.identity import DefaultAzureCredential
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.web import WebSiteManagementClient
from azure.keyvault.secrets import SecretClient

# Authenticate with Azure using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create the Resource Management and WebSite Management clients
resource_client = ResourceManagementClient(credential, "<subscription_id>")
web_client = WebSiteManagementClient(credential, "<subscription_id>")

# Set environment variables for the app
resource_group_name = "your_resource_group_name"
app_name = "your_app_name"

web_client.web_apps.update_application_settings(
    resource_group_name,
    app_name,
    {"MY_VARIABLE": "my_value"}
)

# Set application setting for the app
web_client.web_apps.update_application_settings(
    resource_group_name,
    app_name,
    {"SETTING_NAME": "setting_value"}
)

# Manage secrets with Azure Key Vault
key_vault_name = "your_key_vault_name"
secret_name = "your_secret_name"
secret_value = "your_secret_value"

# Create a SecretClient
secret_client = SecretClient(vault_url=f"https://{key_vault_name}.vault.azure.net/", credential=credential)

# Set the secret value in Azure Key Vault
secret_client.set_secret(secret_name, secret_value)

# Update an application setting with the secret value
app_settings = web_client.web_apps.list_application_settings(resource_group_name, app_name)
app_settings["SECRET_SETTING"] = secret_client.get_secret(secret_name).value
web_client.web_apps.update_application_settings(resource_group_name, app_name, app_settings)

print("Configuration management completed successfully!")
