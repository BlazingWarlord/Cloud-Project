import paramiko

def connection(hostname,username,password):

    client=paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(hostname,username=username,password=password)

    stdin,stdout,stderr=client.exec_command('powershell -Command \"[System.Environment]::OSVersion.VersionString\"')
    os=stdout.read().decode().splitlines()

    stdin,stdout,stderr=client.exec_command('powershell -Command \"Get-Process\"')
    proc=stdout.read().decode().splitlines()

    stdin,stdout,stderr=client.exec_command('powershell -Command \"Get-NetTCPConnection | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State\"')
    open_ports=stdout.read().decode().splitlines()

    client.close()
    return [os,proc,open_ports]

def predict_server_type(running_applications, open_ports):
    # Mapping of application to server type
    application_server_mapping = {
        "web": ["80", "443"],
        "database": ["3306", "5432"],
        "file_server": ["21", "22"],
        "mail": ["25", "143", "110"],
    }

    # Check if any known application's ports are open
    for application, ports in application_server_mapping.items():
        if set(ports).intersection(open_ports):
            return application

    # If no known application's ports are open, suggest a generic server type
    return "generic_server"


# Example usage with Paramiko data
running_applications = ["web", "database"]
open_ports = ["80", "443"]

connection("localhost","Sharan","3021")

predicted_server_type = predict_server_type(running_applications, open_ports)
print("Predicted Server Type:", predicted_server_type)

