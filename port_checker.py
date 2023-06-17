import socket

def find_open_ports(ip_address, start_port, end_port):
    open_ports = []
    
    for port in range(start_port, end_port + 1):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)  # Set a timeout value for the connection attempt
        
        result = sock.connect_ex((ip_address, port))
        if result == 0:
            open_ports.append(port)
        
        sock.close()

    return open_ports

# Example usage
target_ip = 'localhost'  # Replace with the target IP address
start_port = 1
end_port = 65000  # Upper limit for port scanning

open_ports = find_open_ports(target_ip, start_port, end_port)

print("Open ports:")
for port in open_ports:
    print(port)


