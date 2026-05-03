import socket
import psutil


def collect_network_info():
    result = []

    for name, addresses in psutil.net_if_addrs().items():
        ips = [a for a in addresses if a.family == socket.AF_INET]

        for addr in ips:
             result.append((name, addr.address, addr.netmask))

    return result


def main():
    data = collect_network_info()

    for iface, ip, mask in data:
        print(f"[{iface}] {ip} / {mask}")


if __name__ == "__main__":
    main()