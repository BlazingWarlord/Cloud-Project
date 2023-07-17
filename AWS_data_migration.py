import boto3
from azure.storage.blob import BlobServiceClient

# AWS credentials
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
aws_region = 'us-west-2'  # Replace with your AWS region

# Azure credentials
azure_storage_connection_string = 'YOUR_AZURE_STORAGE_CONNECTION_STRING'
azure_container_name = 'YOUR_AZURE_CONTAINER_NAME'

# AWS S3 client
s3_client = boto3.client('s3', region_name=aws_region,
                         aws_access_key_id=aws_access_key_id,
                         aws_secret_access_key=aws_secret_access_key)

# Azure Blob Storage client
blob_service_client = BlobServiceClient.from_connection_string(azure_storage_connection_string)
container_client = blob_service_client.get_container_client(azure_container_name)

# AWS S3 bucket and key
aws_bucket_name = 'YOUR_AWS_BUCKET_NAME'
aws_key = 'YOUR_AWS_OBJECT_KEY'

# Download the AWS VM data
s3_client.download_file(aws_bucket_name, aws_key, 'downloaded_data.vhd')

# Upload the data to Azure Blob Storage
with open('downloaded_data.vhd', 'rb') as data:
    container_client.upload_blob(name='migrated_data.vhd', data=data)

print('AWS VM data migration to Azure completed.')
