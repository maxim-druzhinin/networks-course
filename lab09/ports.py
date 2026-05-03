import socket
import sys

def find_free_ports(ip, start_port, end_port):
    free_ports = []
    for port in range(start_port, end_port + 1):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.15)
                result =s.connect_ex((ip, port))

                if result != 0:
                    free_ports.append(port)

        except socket.error:
            continue
    return free_ports


def main():
    try:
        ip = sys.argv[1]
        start_port = int(sys.argv[2])
        end_port= int(sys.argv[3])
    except (IndexError, ValueError):
        print("Use: python script.py <ip> <start_port> <end_port>")
        return

    try:
        ports = find_free_ports(ip, start_port, end_port)
    except socket.gaierror:
        print("Invalid IP address")
        return

    print(f"Free ports on {ip}:")
    for p in ports:
        print(p)


if __name__ == "__main__":
    main()