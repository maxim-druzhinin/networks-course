import os
import socket
import struct
import time
import statistics

ICMP_ECHO_REQUEST = 8
ICMP_ECHO_REPLY =0
ICMP_DEST_UNREACHABLE = 3
ICMP_TIME_EXCEEDED = 11
DATA_SIZE= 56

UNREACHABLE_CODES = {
    0: "Network Unreachable",
    1: "Host Unreachable",
    2: "Protocol Unreachable",
    3: "Port Unreachable",
}


def checksum(data):
    if len(data) % 2:
        data += b"\x00"
    total = sum(int.from_bytes(data[i:i + 2], "big") for i in range(0, len(data), 2))
    while total > 0xFFFF:
        total = (total & 0xFFFF) + (total >> 16)
    return (~total) & 0xFFFF


def create_packet(identifier, sequence):
    header  = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, 0, identifier, sequence)
    payload = struct.pack("!d", time.time()) + bytes(DATA_SIZE - 8)
    header  = struct.pack("!BBHHH", ICMP_ECHO_REQUEST, 0, checksum(header + payload), identifier, sequence)
    return header + payload

def receive_reply(sock, identifier, sequence):
    deadline = time.time() + 1
    while True:
        sock.settimeout(deadline - time.time())
        try:
            packet, (ip, _) = sock.recvfrom(1024)
            recv_time = time.time()
        except socket.timeout:
            return None

        ihl = (packet[0] & 0x0F) * 4
        icmp_type, code, _, recv_id, recv_seq = struct.unpack("!BBHHH", packet[ihl:ihl + 8])

        if icmp_type == ICMP_ECHO_REPLY and recv_id == identifier and recv_seq == sequence:
            sent_time = struct.unpack("!d", packet[ihl + 8:ihl + 16])[0]
            return {"ip": ip, "bytes": len(packet) - ihl, "ttl": packet[8], "rtt": recv_time - sent_time}

        if icmp_type in (ICMP_DEST_UNREACHABLE, ICMP_TIME_EXCEEDED):
            inner_ihl = (packet[ihl + 8] & 0x0F) * 4
            _, _, _, inner_id, inner_seq = struct.unpack("!BBHHH", packet[ihl + 8 + inner_ihl:ihl + 16 + inner_ihl])
            if inner_id == identifier and inner_seq == sequence:
                return {"error": True, "type": icmp_type, "code": code, "ip": ip}

        if deadline - time.time() <= 0:
            return None


def ping(host):
    dest_ip    = socket.gethostbyname(host)
    identifier = os.getpid() & 0xFFFF
    sent = received = 0
    rtts = []

    print(f"PING {host} ({dest_ip}): {DATA_SIZE} data bytes")

    with socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP) as sock:
        for seq in range(10):
            sock.sendto(create_packet(identifier, seq), (dest_ip, 0))
            sent += 1
            reply = receive_reply(sock, identifier, seq)

            if reply is None:
                print(f"Request timeout for icmp_seq {seq}")
            elif reply.get("error"):
                if reply["type"] == ICMP_DEST_UNREACHABLE:
                    reason = UNREACHABLE_CODES.get(reply["code"], f"Unknown code {reply['code']}")
                    print(f"From {reply['ip']}: icmp_seq={seq} Destination Unreachable — {reason}")
                else:
                    print(f"From {reply['ip']}: icmp_seq={seq} Time to Live exceeded")
            else:
                received += 1
                rtts.append(reply["rtt"])
                print(f'{reply["bytes"]} bytes from {reply["ip"]}: icmp_seq={seq} ttl={reply["ttl"]} time={reply["rtt"] * 1000:.3f} ms')

            time.sleep(1)

    loss = (sent - received) / sent * 100
    print(f"\n--- {host} ping statistics ---")
    print(f"{sent} packets transmitted, {received} packets received, {loss:.1f}% packet loss")

    if rtts:
        ms = [r * 1000 for r in rtts]
        stddev = statistics.pstdev(ms) if len(ms) > 1 else 0.0
        print(f"round-trip min/avg/max/stddev = {min(ms):.3f}/{statistics.mean(ms):.3f}/{max(ms):.3f}/{stddev:.3f} ms")


if __name__ == "__main__":
    ping(input("Enter host: "))