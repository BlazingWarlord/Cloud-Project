import platform
import subprocess

def get_server_os(ip_address):
    try:
        output = subprocess.check_output(['ping', '-c', '1', ip_address])
        if platform.system() == 'Windows':
            ttl = int(output.split(b'TTL=')[1].split()[0])
        elif platform.system() == 'Linux':
            ttl = int(output.split(b'ttl=')[1].split()[0])
        else:
            return 'Unknown'

        if ttl <= 64:
            return 'Linux'
        elif ttl <= 128:
            return 'Windows'
        elif ttl <= 255:
            return 'Unix'

    except subprocess.CalledProcessError:
        return 'Unknown'

# Example usage
target_ip = '23.45.160.244'  # Replace with the target IP address

os_name = get_server_os(target_ip)
print(f"Operating System: {os_name}")
