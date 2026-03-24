import socket
import sys
import os


def get_content_type(filename):
    content_types = {
        ".html": "text/html; charset=utf-8",
        ".htm": "text/html; charset=utf-8",
        ".txt": "text/plain; charset=utf-8",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".png": "image/png",
    }

    ext = os.path.splitext(filename)[1].lower()
    return content_types.get(ext, "application/octet-stream")


def build_response(status_code, status_text, body=b"", content_type="text/plain; charset=utf-8"):
    headers = [
        f"HTTP/1.1 {status_code} {status_text}",
        f"Content-Length: {len(body)}",
        f"Content-Type: {content_type}",
        "Connection: close",
        "",
        ""
    ]
    return "\r\n".join(headers).encode("utf-8") + body


def run_server(port):
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", port))
    server_socket.listen(1)

    print(f"Server is running on port {port}")

    while True:
        connection_socket, _ = server_socket.accept()

        request = connection_socket.recv(4096).decode("utf-8", errors="ignore")

        if not request:
            connection_socket.close()
            continue

        request_line = request.splitlines()[0]
        parts = request_line.split()

        method = parts[0]
        path = parts[1]

        if method != "GET":
            response = build_response(405, "Method Not Allowed", b"405 Method Not Allowed")
            connection_socket.sendall(response)
            connection_socket.close()
            continue

        filename = path.lstrip("/")

        if os.path.isfile(filename):
            with open(filename, "rb") as f:
                body = f.read()
            content_type = get_content_type(filename)
            response = build_response(200, "OK", body, content_type)
        else:
            body = b"<html><body><h1>404 Not Found</h1></body></html>"
            response = build_response(404, "Not Found", body, "text/html; charset=utf-8")

        connection_socket.sendall(response)
        connection_socket.close()


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python server.py <port>")
        sys.exit(1)

    port = int(sys.argv[1])
    run_server(port)