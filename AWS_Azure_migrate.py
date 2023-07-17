from azure.identity import DefaultAzureCredential
from azure.mgmt.migrate import MigrateProjectOperations, MigrateAssessmentOperations, \
    MigrateGroupOperations, MigrateItemOperations
from azure.mgmt.migrate.models import AssessedItemDetails, CreateMigrateProjectInput, \
    CreateAssessmentInput, CreateGroupInput, CreateMigrateInput, MigrateProject, \
    UpdateMigrateProjectInput, CreateMachineDiscoveryInput, MigrateDiscovery
import requests
import time

# Azure credentials
azure_subscription_id = 'YOUR_AZURE_SUBSCRIPTION_ID'
azure_location = 'westus2'  # Replace with your Azure location

# Azure Migrate credentials
credential = DefaultAzureCredential()
migrate_project_operations = MigrateProjectOperations(credential, azure_subscription_id)
migrate_assessment_operations = MigrateAssessmentOperations(credential, azure_subscription_id)
migrate_group_operations = MigrateGroupOperations(credential, azure_subscription_id)
migrate_item_operations = MigrateItemOperations(credential, azure_subscription_id)

# Create an Azure Migrate project
project_name = 'YOUR_PROJECT_NAME'
project_resource_group = 'YOUR_AZURE_RESOURCE_GROUP'

project_input = CreateMigrateProjectInput(
    location=azure_location,
    group_name=project_resource_group,
    name=project_name,
    refresh_summary=True
)

project = migrate_project_operations.create_or_update(
    project_name,
    project_input
)

# Wait for the project to be provisioned
while project.provisioning_state != 'Succeeded':
    time.sleep(10)
    project = migrate_project_operations.get(project_name)

# Create an Azure Migrate assessment
assessment_name = 'YOUR_ASSESSMENT_NAME'
assessment_input = CreateAssessmentInput(
    location=azure_location,
    assessment_type='Database',
    source='AWS',
    source_resource_group='YOUR_AWS_RESOURCE_GROUP',
    target_resource_group=project_resource_group,
    project_id=project.id,
    name=assessment_name
)

assessment = migrate_assessment_operations.create_or_update(
    project_name,
    assessment_name,
    assessment_input
)

# Wait for the assessment to complete
while assessment.provisioning_state != 'Succeeded':
    time.sleep(10)
    assessment = migrate_assessment_operations.get(project_name, assessment_name)

# Create an Azure Migrate group
group_name = 'YOUR_GROUP_NAME'
group_input = CreateGroupInput(
    location=azure_location,
    project_id=project.id,
    name=group_name
)

group = migrate_group_operations.create_or_update(
    project_name,
    group_name,
    group_input
)

# Wait for the group to be provisioned
while group.provisioning_state != 'Succeeded':
    time.sleep(10)
    group = migrate_group_operations.get(project_name, group_name)

# Discover the AWS VMs
discovery_input = CreateMachineDiscoveryInput(
    discovery_type='Azure',
    machine_name='AWSDiscovery',
    discovery_properties={'Region': 'us-west-2'}  # Replace with your AWS region
)

discovery = migrate_item_operations.create_or_update_discovery(
    project_name,
    group_name,
    discovery_input
)

# Wait for the discovery to complete
while discovery.provisioning_state != 'Succeeded':
    time.sleep(10)
    discovery = migrate_item_operations.get_discovery(project_name, group_name, discovery.machine_name)

# Create the migration
migration_name = 'YOUR_MIGRATION_NAME'
migration_input = CreateMigrateInput(
    location=azure_location,
    assessment_id=assessment.id,
    source_resource_group='YOUR_AWS_RESOURCE_GROUP',
    target_resource_group=project_resource_group,
    project_id=project.id,
    name=migration_name
)

migration = migrate_item_operations.create_or_update_migration(
    project_name,
    group_name,
    migration_name,
    migration_input
)

# Wait for the migration to complete
while migration.provisioning_state != 'Succeeded':
    time.sleep(10)
    migration = migrate_item_operations.get_migration(project_name, group_name, migration_name)

print('Database server migration from AWS to Azure initiated.')
