import os
from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
import boto3

# AWS credentials
AWS_ACCESS_KEY_ID = "your_aws_access_key_id"
AWS_SECRET_ACCESS_KEY = "your_aws_secret_access_key"
AWS_REGION = "your_aws_region"

# Azure credentials and settings
AZURE_SUBSCRIPTION_ID = "your_azure_subscription_id"
AZURE_RESOURCE_GROUP = "your_azure_resource_group"
AZURE_LOCATION = "your_azure_location"

# Function to create an Azure VM
def create_azure_vm(vm_name, vm_size, os_username, os_password, image_reference):
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, AZURE_SUBSCRIPTION_ID)

    # Set VM properties
    vm_parameters = {
        "location": AZURE_LOCATION,
        "os_profile": {
            "computer_name": vm_name,
            "admin_username": os_username,
            "admin_password": os_password,
        },
        "hardware_profile": {"vm_size": vm_size},
        "storage_profile": {
            "image_reference": image_reference,
        },
    }

    # Create VM
    async_vm_creation = compute_client.virtual_machines.create_or_update(
        AZURE_RESOURCE_GROUP, vm_name, vm_parameters
    )
    async_vm_creation.wait()


# Function to get AWS VM details
def get_aws_vm_details():
    ec2_client = boto3.client(
        "ec2",
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION,
    )

    # Replace "your_instance_id" with the actual instance ID of the AWS VM you want to migrate
    response = ec2_client.describe_instances(InstanceIds=["your_instance_id"])

    if not response["Reservations"]:
        raise ValueError("AWS VM not found.")

    vm_details = response["Reservations"][0]["Instances"][0]
    return vm_details


# Function to get a list of available Azure VM images
def get_azure_vm_images():
    credential = DefaultAzureCredential()
    compute_client = ComputeManagementClient(credential, AZURE_SUBSCRIPTION_ID)
    publisher = "Canonical"
    offer = "UbuntuServer"
    sku = "16.04-LTS"

    # List VM images
    vm_images = compute_client.virtual_machine_images.list(
        AZURE_LOCATION, publisher, offer, sku, "latest"
    )
    return list(vm_images)


# Function to interactively choose an Azure VM image
def choose_azure_vm_image(azure_vm_images):
    print("Available Azure VM images:")
    for i, vm_image in enumerate(azure_vm_images, start=1):
        print(f"{i}. {vm_image.name}")

    while True:
        choice = input("Choose an Azure VM image (enter the number): ")
        try:
            index = int(choice)
            if 1 <= index <= len(azure_vm_images):
                return azure_vm_images[index - 1].id
        except ValueError:
            pass

        print("Invalid choice. Please select a valid number.")


# Function to migrate AWS VM to Azure
def migrate_aws_vm_to_azure():
    # Step 1: Get AWS VM details
    aws_vm_details = get_aws_vm_details()

    # Extract relevant AWS VM details
    aws_vm_size = aws_vm_details["InstanceType"]
    aws_os_username = aws_vm_details["KeyName"]  # Use the key name if using key pair
    aws_os_password = "your_os_password"  # Replace with actual OS password or key pair

    # Step 2: Get a list of available Azure VM images
    azure_vm_images = get_azure_vm_images()

    # Step 3: Choose an Azure VM image
    image_reference = choose_azure_vm_image(azure_vm_images)

    # Step 4: Create Azure VM
    create_azure_vm(
        aws_vm_details["Name"],
        aws_vm_size,
        aws_os_username,
        aws_os_password,
        image_reference,
    )

    print("Migration completed successfully.")


if __name__ == "__main__":
    migrate_aws_vm_to_azure()
