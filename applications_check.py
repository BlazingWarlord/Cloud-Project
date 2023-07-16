import paramiko
import subprocess
import ipaddress

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

def check_range_ip(start_ip,end_ip,username,password):
    ip_range = ipaddress.summarize_address_range(ipaddress.IPv4Address(start_ip), ipaddress.IPv4Address(end_ip))
    ips_within_range = []

    for ip_network in ip_range:
        ips_within_range.extend(str(ip) for ip in ip_network)

    result_data = {}
    
    for ip in ips_within_range:
        try:
            results = connection(ip,username,password)
            result_data[ip] = results
        except:
            pass
    return result_data if len(result_data) > 0 else "No IPs detected in range"


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

    result_percentages = []

    result[0].extend(result[1])
    percentage_set = set(result[0])
    
    for i in percentage_set:
        result_percentages.append((i,(result[0].count(i)/len(result[0]))*100))

    sorted_result_percentages = sorted(result_percentages, key = lambda x:x[1], reverse = True)

    # If no known application's ports are open, suggest a generic server type
    return sorted_result_percentages if len(result_percentages) > 0 else "generic_server"


# Example usage with Paramiko data
running_applications = ["web", "database"]
open_ports = ["80", "443"]

l = connection("localhost","11110","Blazing123")

predicted = predict_server_type(l[1],l[2])

print(predicted)

l = self_assess()

l = check_range_ip('192.168.1.2','192.168.1.7','11110','Blazing123')

print(l)






