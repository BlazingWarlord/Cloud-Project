from azure.storage.blob import BlobServiceClient
from azure.storage.blob._generated.models import StorageTransferOptions

def transfer_data_with_data_box(connection_string, container_name, local_file_path, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    with open(local_file_path, "rb") as file:
        options = StorageTransferOptions(block_size=4 * 1024 * 1024)  # Configure the block size (optional)
        container_client.upload_blob(name=blob_name, data=file, transfer_options=options)

# Example usage
connection_string = "<Azure Blob Storage connection string>"
container_name = "<Container name>"
local_file_path = "<Path to local file>"
blob_name = "<Name for the blob in Azure>"
transfer_data_with_data_box(connection_string, container_name, local_file_path, blob_name)