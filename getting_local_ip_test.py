import socket

def get_local_ip_addresses():
    try:
        # Attempt to get all network interfaces
        interfaces = socket.if_nameindex()
        
        if not interfaces:
            print("No active network interfaces found.")
            return []
        
        ip_addresses = []
        for index, interface_name in interfaces:
            # Skip the loopback interface
            if interface_name.lower() == 'lo':
                continue
            
            # Try to get the IP address for the interface
            try:
                # Attempt to get both IPv4 and IPv6 addresses
                ipv4_address = socket.inet_ntoa(socket.inet_pton(socket.AF_INET, socket.gethostbyname(interface_name)))
                ipv6_address = socket.inet_ntop(socket.AF_INET6, socket.inet_pton(socket.AF_INET6, socket.gethostbyname(interface_name)))
                
                # Add both addresses if they exist; otherwise, add just the one that exists
                if ipv4_address:
                    ip_addresses.append(ipv4_address)
                if ipv6_address:
                    ip_addresses.append(ipv6_address)
            except OSError as e:
                # Handle exception for non-IPv4/IPv6 addresses
                print(f"Error getting IP address for {interface_name}: {e}")
                continue
        
        return ip_addresses
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

# Example usage
ip_addresses = get_local_ip_addresses()
if ip_addresses:
    print("Local IP Addresses:", ip_addresses)
else:
    print("Unable to retrieve local IP addresses.")
