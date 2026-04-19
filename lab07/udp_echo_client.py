import time
import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 11111
TIMEOUT = 1
PING_COUNT = 10

client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
client_socket.settimeout(TIMEOUT)

sent_packets = 0
received_packets = 0
rtts = []

print(f"Pinging {SERVER_HOST}:{SERVER_PORT} with UDP:")

for seq in range(1, PING_COUNT + 1):
    send_time = time.time()
    message = f"Ping {seq} {send_time}"
    sent_packets += 1

    try:
        client_socket.sendto(message.encode(), (SERVER_HOST, SERVER_PORT))
        response, server_address = client_socket.recvfrom(1024)
        receive_time = time.time()

        rtt = receive_time - send_time
        rtts.append(rtt)
        received_packets += 1

        print(f"Reply from {server_address[0]}:{server_address[1]}: "
              f"bytes={len(response)} seq={seq} time={rtt:.6f} s")

    except socket.timeout:
        print(f"Request timed out for seq={seq}")

client_socket.close()

lost_packets = sent_packets - received_packets
loss_percent = (lost_packets / sent_packets) * 100

print()
print(f"--- {SERVER_HOST} ping statistics ---")
print(f"{sent_packets} packets transmitted, {received_packets} packets received, {loss_percent:.0f}% packet loss")

if rtts:
    min_rtt = min(rtts)
    max_rtt = max(rtts)
    avg_rtt = sum(rtts) / len(rtts)
    print(f"round-trip min/avg/max = {min_rtt:.6f}/{avg_rtt:.6f}/{max_rtt:.6f} s")