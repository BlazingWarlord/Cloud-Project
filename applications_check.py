import paramiko

hostname='192.168.141.200'
username='Sharan'
password='3021'

client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname,username=username,password=password)

stdin,stdout,stderr=client.exec_command('powershell -Command \"[System.Environment]::OSVersion.VersionString\"')
os=stdout.read().decode().splitlines()

stdin,stdout,stderr=client.exec_command('powershell -Command \"Get-Process\"')
proc=stdout.read().decode().splitlines()

stdin,stdout,stderr=client.exec_command('powershell -Command \"Get-NetTCPConnection | Select-Object LocalAddress,LocalPort,RemoteAddress,RemotePort,State\"')
open_ports=stdout.read().decode().splitlines()

print("OS:")
for i in os:
    print(i)

print("Process: ")
for pro in proc:
    print(pro)

print("\nOpen ports:")
for ports in open_ports:
    print(ports)

client.close()

