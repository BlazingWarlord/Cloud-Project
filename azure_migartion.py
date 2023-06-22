from azure.identity import DefaultAzureCredential
from azure.mgmt.compute import ComputeManagementClient
from azure.mgmt.resource import ResourceManagementClient
from azure.mgmt.migrate import MigrateManagementClient
from azure.mgmt.migrate.models import AsrHyperVSiteDetails, AsrHyperVSiteSettings, AsrVmmDetails, AsrVmmFabricDetails
from azure.core.exceptions import HttpResponseError

# Authenticate using default credentials
credential = DefaultAzureCredential()

#subsciption id
subscription_id = ""
resource_group_name = ""

# Create clients for resource management and compute management
resource_client = ResourceManagementClient(credential, subscription_id)
compute_client = ComputeManagementClient(credential, subscription_id)

# Create a client for Azure Migrate management
migrate_client = MigrateManagementClient(credential, subscription_id)

project_name = ""
location = 'eastus' 

try:
    # Create the migration project
    migration_project = migrate_client.migration_projects.create_or_update(
        resource_group_name,
        project_name,
        {
            'location': location
        }
    )

    # Specify the source server details
    source_vm_name = ""
    source_vm_resource_group = ""
    source_hyperv_site_name = ""
    source_hyperv_site_fqdn = ""

    # Create the Hyper-V site details
    hyperv_site_details = AsrHyperVSiteDetails(
        site_id= "",
        friendly_name=source_hyperv_site_name,
        hypervisor_id=source_hyperv_site_fqdn
    )

    # Create the Hyper-V site settings
    hyperv_site_settings = AsrHyperVSiteSettings(
        vmware_v_center_fqdn=None,
        hyperv_site_details=hyperv_site_details
    )

    # Create the VMM details
    vmm_details = AsrVmmDetails(
        fabric_id= "",
        friendly_name= "",
        vmm_managed=None,
        vmm_server_fqdn=None,
        vmm_server_privileged_account=None
    )

    # Create the VMM fabric details
    vmm_fabric_details = AsrVmmFabricDetails(
        vmm_fabric_id= "",
        friendly_name= "",
        vmm_details=vmm_details
    )

    # Create the discovery settings
    discovery_settings = {
        'source_vm_name': source_vm_name,
        'source_vm_resource_group': source_vm_resource_group,
        'discovery_solution': 'HyperVAndVMM',
        'hvr_vmm_details': vmm_fabric_details,
        'hvr_hyper_v_site_details': hyperv_site_settings
    }

    # Create the assessment
    assessment = migrate_client.assessments.create_or_update(
        resource_group_name,
        project_name,
        'assessment01',
        discovery_settings
    )

    print("Assessment created successfully.")

except HttpResponseError as ex:
    print(f"An error occurred: {ex}")
