import socket
import sys


def build_request(host, port, filename):
    return (
        f"GET /{filename} HTTP/1.1\r\n"
        f"Host: {host}:{port}\r\n"
        f"Connection: close\r\n"
        f"\r\n"
    )


def parse_response(response):
    header_bytes, body = response.split(b"\r\n\r\n", 1)
    headers_text = header_bytes.decode("utf-8", errors="ignore")
    return headers_text, body


def get_status_code(headers_text):
    first_line = headers_text.splitlines()[0]
    return first_line.split()[1]


def get_content_type(headers_text):
    for line in headers_text.splitlines():
        if line.startswith("Content-Type:"):
            return line.split(":", 1)[1].strip().split(";")[0]
    return ""


def run_client(host, port, filename):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((host, port))

    print(f"Connected to {host}:{port}")

    request = build_request(host, port, filename)
    client_socket.sendall(request.encode("utf-8"))

    response = b""
    while True:
        packet = client_socket.recv(4096)
        if not packet:
            break
        response += packet

    client_socket.close()

    headers_text, body = parse_response(response)

    print("\nHeaders:")
    print(headers_text)

    status_code = get_status_code(headers_text)
    content_type = get_content_type(headers_text)

    if status_code == "200":
        if content_type.startswith("text"):
            print("\nFile content:")
            print(body.decode("utf-8", errors="ignore"))
        else:
            with open(filename, "wb") as f:
                f.write(body)
            print(f"\nFile {filename} was successfully saved.")
    else:
        print("\nFile content:")
        print(body.decode("utf-8", errors="ignore"))


if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python client.py <server_host> <server_port> <filename>")
        sys.exit(1)

    host = sys.argv[1]
    port = int(sys.argv[2])
    filename = sys.argv[3]

    run_client(host, port, filename)