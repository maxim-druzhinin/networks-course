import socket
import time
from datetime import datetime

BROADCAST_IP = "255.255.255.255"
PORT = 8888

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

    print(f"UDP broadcast server started on port {PORT}")

    while True:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"Server time: {current_time}"
        server_socket.sendto(message.encode(), (BROADCAST_IP, PORT))
        print(f"Sent: {message}")
        time.sleep(1)

if __name__ == "__main__":
    start_server()