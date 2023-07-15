import paramiko
import subprocess

def self_assess():
    cmd="powershell -Command [System.Environment]::OSVersion.VersionString"
    os=subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

    cmd = "powershell -Command Get-Process"  
    proc = subprocess.run(cmd, shell=True, capture_output=True, text=True).stdout

    print(proc)

    command = "Get-NetTCPConnection | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State"
    open_ports = subprocess.run(['powershell.exe', '-Command', command], capture_output=True, text=True).stdout


    splitted = open_ports.split('\n')
    open_ = []
    for port in splitted:
        if 'LocalPort' in port:
            open_.append(port.split(':')[1])
        

    return [os,proc,open_]

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
    open_ = []
    for port in open_ports:
        if 'LocalPort' in port:
            open_.append(port.split(':')[1])
            

    client.close()
    return [os,proc,open_]

def predict_server_type(running_applications, open_ports):
    # Mapping of application to server type
    application_server_mapping = {
        "web": [" 80", " 443"],
        "database": [" 3306", " 5432"],
        "file_server": [" 21", " 22"],
        "mail": [" 25", " 143", " 110"],
    }


    apps_application = []

    apps = {('nginx','apache','tomcat'):"web",('mysql','postgresql','mongodb'):"database",("filezilla","samba", "nfs", "ftp"):"file_server",("postfix", "exim", "sendmail"):"Mail"}
    
    for app in running_applications:
        app = app.lower()
        for possible in apps:
            for app_ in possible:
                if app_ in app:
                    apps_application.append(apps[possible])
                    
        
        

    apps_port = []

    for application, ports in application_server_mapping.items():
        if set(ports).intersection(set(open_ports)):
            apps_port.append(application)

    result = [apps_port,apps_application]

    result[0].extend(result[1])
    percentage_set = set(result[0])

    print("Percentage of predictions: \n")
    
    for i in percentage_set:
        print(f"{i}: {(result[0].count(i)/len(result[0]))*100}%")

    # If no known application's ports are open, suggest a generic server type
    return result if len(apps_port) > 0 or len(apps_application) > 0 else "generic_server"


# Example usage with Paramiko data
running_applications = ["web", "database"]
open_ports = ["80", "443"]

l = connection("localhost","11110","Blazing123")

predicted_server_type = predict_server_type(l[1],l[2])

l = self_assess()

print(l[1])

predict_server_type(l[1],l[2])


