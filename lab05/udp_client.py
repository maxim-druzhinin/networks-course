import socket

PORT = 8888
BUFFER_SIZE = 1024

def start_client():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(("", PORT))

    print(f"UDP client listening on port {PORT}...")

    while True:
        data, addr = client_socket.recvfrom(BUFFER_SIZE)
        print(f"From {addr}: {data.decode()}")

if __name__ == "__main__":
    start_client()