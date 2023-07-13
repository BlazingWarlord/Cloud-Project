#pip install azure-storage-file-datalake
import os
from azure.identity import DefaultAzureCredential
from azure.storage.filedatalake import DataLakeServiceClient

def sync_directories_with_data_lake(connection_string, local_directory, data_lake_filesystem, destination_directory):
    credential = DefaultAzureCredential()
    service_client = DataLakeServiceClient(account_url=connection_string, credential=credential)
    filesystem_client = service_client.get_file_system_client(data_lake_filesystem)
    directory_client = filesystem_client.get_directory_client(destination_directory)
    
    for root, _, files in os.walk(local_directory):
        for file in files:
            local_file_path = os.path.join(root, file)
            destination_file_path = os.path.join(destination_directory, file)
            directory_client.upload_file(destination_file_path, local_file_path)
            print(f"Uploaded {local_file_path} to {destination_file_path}")

# Example usage
connection_string = "<Azure Data Lake Storage connection string>"
local_directory = "<Path to local directory>"
data_lake_filesystem = "<Data Lake filesystem name>"
destination_directory = "<Destination directory in Data Lake>"
sync_directories_with_data_lake(connection_string, local_directory, data_lake_filesystem, destination_directory)
