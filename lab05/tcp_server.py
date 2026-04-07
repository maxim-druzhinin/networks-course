import socket
import subprocess

SERVER_HOST = "0.0.0.0"
SERVER_PORT = 8888
END_MARKER = b"\0"


def execute_command(command: str):
    process = subprocess.Popen(
        command,
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    for line in process.stdout:
        yield line

    for line in process.stderr:
        yield line

    yield f"\n[return code: {process.wait()}]\n"


def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((SERVER_HOST, SERVER_PORT))
    server_socket.listen(5)

    print(f"Server started on {SERVER_HOST}:{SERVER_PORT}")

    while True:
        client_socket, client_address = server_socket.accept()
        print(f"New connection: {client_address}")

        with client_socket:
            while True:
                data = client_socket.recv(1024)
                if not data:
                    print("Client disconnected")
                    break

                command = data.decode().strip()
                print(f"Command: {command}")

                if command.lower() == "quit":
                    client_socket.sendall("Connection closed\n".encode())
                    client_socket.sendall(END_MARKER)
                    break

                try:
                    for output in execute_command(command):
                        client_socket.sendall(output.encode())
                except Exception as e:
                    client_socket.sendall(f"Error: {e}\n".encode())

                client_socket.sendall(END_MARKER)


if __name__ == "__main__":
    start_server()