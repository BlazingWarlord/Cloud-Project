from azure.storage.blob import BlobServiceClient, BlobType

def upload_to_blob_storage(connection_string, container_name, local_file_path, blob_name):
    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    container_client = blob_service_client.get_container_client(container_name)
    
    with open(local_file_path, "rb") as file:
        container_client.upload_blob(name=blob_name, data=file, blob_type=BlobType.BlockBlob)

# Example usage
connection_string = "<Azure Blob Storage connection string>"
container_name = "<Container name>"
local_file_path = "<Path to local file>"
blob_name = "<Name for the blob in Azure>"
upload_to_blob_storage(connection_string, container_name, local_file_path, blob_name)