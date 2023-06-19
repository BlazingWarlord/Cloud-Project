import paramiko

hostname=''
username=''
password=''

client=paramiko.SSHClient()
client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
client.connect(hostname,username=username,password=password)

stdin,stdout,stderr=client.exec_command('ps aux --no-headers')
running_processes=stdout.read().decode().splitlines()

stdin,stdout,stderr=client.exec_command('netstat -an | grep LISTEN')
open_ports=stdout.read().decode().splitlines()

print("Running prcesses:")
for process in running_processes:
    print(process)

print("\nOpen ports:")
for ports in open_ports:
    print(ports)

client.close()