import socket

SERVER_HOST = "127.0.0.1"
SERVER_PORT = 8888
END_MARKER = b"\0"


def receive_response(sock: socket.socket) -> str:
    data = b""
    while True:
        chunk = sock.recv(1024)
        if not chunk:
            break
        if END_MARKER in chunk:
            data += chunk.split(END_MARKER)[0]
            break
        data += chunk
    return data.decode(errors="replace")


def start_client():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
        client_socket.connect((SERVER_HOST, SERVER_PORT))
        print(f"Connected to {SERVER_HOST}:{SERVER_PORT}")

        while True:
            command = input("Enter command (or quit): ").strip()
            if not command:
                continue

            client_socket.sendall(command.encode())
            response = receive_response(client_socket)

            print("\n=== Server response ===")
            print(response)

            if command.lower() == "quit":
                break


if __name__ == "__main__":
    start_client()