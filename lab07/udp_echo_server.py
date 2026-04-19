import random
import socket

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 11111

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind((SERVER_HOST, SERVER_PORT))

print(f"UDP server is running on {SERVER_HOST}:{SERVER_PORT}")

while True:
    message, client_address = server_socket.recvfrom(1024)

    if random.random() < 0.15:
        print(f"Packet from {client_address} lost")
        continue

    modified_message = message.decode().upper().encode()
    server_socket.sendto(modified_message, client_address)
    print(f"Replied to {client_address}: {modified_message.decode()}")