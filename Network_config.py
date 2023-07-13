from azure.identity import DefaultAzureCredential
from azure.mgmt.network import NetworkManagementClient
from azure.mgmt.network.models import (
    NetworkInterfaceIPConfiguration,
    NetworkSecurityGroup,
    SecurityRule,
    Subnet,
    VirtualNetwork,
)

# Replace with your Azure subscription ID and resource group name
subscription_id = "603f1137-266a-461d-beac-a4d2984f9dc1"
resource_group_name = "VM_1"

# Replace with your Azure credentials
credential = DefaultAzureCredential()

# Initialize the NetworkManagementClient
network_client = NetworkManagementClient(credential, subscription_id)

# Retrieve the network configuration of the source server
source_server_nic_id = "/subscriptions/{subscriptionId}/resourceGroups/{resourceGroupName}/providers/Microsoft.Network/networkInterfaces/{networkInterfaceName}".format(
    subscriptionId="source-subscription-id",
    resourceGroupName="source-resource-group-name",
    networkInterfaceName="source-nic-name"
)
source_nic = network_client.network_interfaces.get(
    resource_group_name=resource_group_name,
    network_interface_name=source_server_nic_id
)

# Create a virtual network in the destination subscription
vnet_name = "my-vnet"
vnet_address_space = source_nic.ip_configurations[0].subnet.address_prefix.split("/")[0] + "/16"
vnet_params = VirtualNetwork(address_space={'address_prefixes': [vnet_address_space]})
vnet = network_client.virtual_networks.begin_create_or_update(resource_group_name, vnet_name, vnet_params).result()

# Create a subnet in the destination subscription
subnet_name = "my-subnet"
subnet_address_space = source_nic.ip_configurations[0].subnet.address_prefix
subnet_params = Subnet(address_prefix=subnet_address_space)
subnet = network_client.subnets.begin_create_or_update(
    resource_group_name,
    vnet_name,
    subnet_name,
    subnet_params
).result()

# Create a network security group in the destination subscription
nsg_name = "my-nsg"
nsg_params = NetworkSecurityGroup()
nsg = network_client.network_security_groups.begin_create_or_update(
    resource_group_name,
    nsg_name,
    nsg_params
).result()

# Create security rules in the destination subscription
for rule in source_nic.network_security_group.security_rules:
    security_rule_params = SecurityRule(
        access=rule.access,
        description=rule.description,
        destination_port_range=rule.destination_port_range,
        direction=rule.direction,
        priority=rule.priority,
        protocol=rule.protocol,
        source_address_prefix=rule.source_address_prefix,
        source_port_range=rule.source_port_range
    )
    security_rule = network_client.security_rules.begin_create_or_update(
        resource_group_name,
        nsg_name,
        rule.name,
        security_rule_params
    ).result()

# Create a network interface in the destination subscription
nic_name = "my-nic"
nic_params = NetworkInterfaceIPConfiguration(
    name=nic_name,
    subnet=subnet,
    public_ip_address=None,  # Replace with a public IP address if needed
    primary=True,
    private_ip_allocation_method="Dynamic",
    private_ip_address_version="IPv4",
    load_balancer_backend_address_pools=None,
    load_balancer_inbound_nat_rules=None,
    load_balancer_frontend_ip_configurations=None,
    application_gateway_backend_address_pools=None,
    application_security_groups=None,
    network_security_group=nsg
)
nic = network_client.network_interfaces.begin_create_or_update(
    resource_group_name,
    nic_name,
    nic_params
).result()

print("Network configuration of the source server in Azure VMs mimicked successfully.")