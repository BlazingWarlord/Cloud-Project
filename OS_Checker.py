import platform
import subprocess

def get_server_os(ip_address):
    output = subprocess.check_output(['ping',ip_address])
    if platform.system() == 'Windows':
        ttl = int(output.split(b'TTL=')[1].split()[0])
    elif platform.system() == 'Linux':
        ttl = int(output.split(b'ttl=')[1].split()[0])
    else:
        return 'UnknowN'

    if ttl <= 64:
        return 'Linux'
    elif ttl <= 128:
        return 'Windows'
    elif ttl <= 255:
        return 'Unix'


target_ip = '10.32.15.51' #IP address

os_name = get_server_os(target_ip)
print(f"Operating System: {os_name}")
