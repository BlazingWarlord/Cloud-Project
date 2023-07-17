import boto3
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.compute.models import VirtualMachineImportParameters

# AWS credentials
aws_access_key_id = 'YOUR_AWS_ACCESS_KEY_ID'
aws_secret_access_key = 'YOUR_AWS_SECRET_ACCESS_KEY'
aws_session_token = 'YOUR_AWS_SESSION_TOKEN'
aws_region = 'us-west-2'  # Replace with your AWS region

# Azure credentials
azure_subscription_id = 'YOUR_AZURE_SUBSCRIPTION_ID'
azure_resource_group = 'YOUR_AZURE_RESOURCE_GROUP'
azure_location = 'westus2'  # Replace with your Azure location

# AWS EC2 client
ec2_client = boto3.client('ec2', region_name=aws_region,
                          aws_access_key_id=aws_access_key_id,
                          aws_secret_access_key=aws_secret_access_key,
                          aws_session_token=aws_session_token)

# Azure compute client
credential = DefaultAzureCredential()
compute_client = ComputeManagementClient(credential, azure_subscription_id)

# AWS EC2 instance details
aws_instance_id = 'YOUR_AWS_INSTANCE_ID'

# Export the AWS instance
export_task = ec2_client.create_instance_export_task(
    Description='Export to Azure',
    ExportToS3Task={
        'ContainerFormat': 'ova',
        'DiskImageFormat': 'vmdk',
        'S3Bucket': 'YOUR_S3_BUCKET',
        'S3Key': 'exported-instance.ova'
    },
    InstanceId=aws_instance_id
)

export_task_id = export_task['ExportTask']['ExportTaskId']

# Wait for the export task to complete
ec2_client.get_waiter('export_task_completed').wait(
    ExportTaskIds=[export_task_id],
    WaiterConfig={
        'Delay': 15,
        'MaxAttempts': 60
    }
)

# Import the VM into Azure
import_params = VirtualMachineImportParameters(
    location=azure_location,
    storage_account_id='YOUR_AZURE_STORAGE_ACCOUNT_ID',
    storage_blob_container_name='YOUR_AZURE_STORAGE_CONTAINER',
    storage_blob_name='imported-instance.ova',
    os_disk={
        'os_type': 'Linux',
        'os_state': 'Generalized'
    },
    network_interfaces=[{
        'id': 'YOUR_AZURE_NETWORK_INTERFACE_ID'
    }]
)

compute_client.virtual_machines.begin_create_or_update(
    azure_resource_group,
    'imported-vm',
    import_params
)

print('VM migration from AWS to Azure initiated.')