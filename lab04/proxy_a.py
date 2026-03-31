import http.server
import logging
import requests

logging.basicConfig(
    filename="proxy.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)


class Proxy(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.handle_request("GET")

    def do_POST(self):
        self.handle_request("POST")

    def handle_request(self, method):
        url = self.path.lstrip("/")
        if not url.startswith("http://"):
            url = "http://" + url

        body = None
        if method == "POST":
            content_length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(content_length) if content_length > 0 else b""

        forward_headers = {}
        for key, value in self.headers.items():
            if key.lower() not in {"host", "content-length", "connection"}:
                forward_headers[key] = value

        try:
            if method == "GET":
                response = requests.get(url, headers=forward_headers, timeout=10)
            else:
                response = requests.post(url, headers=forward_headers, data=body, timeout=10)

            logging.info("URL: %s, Response Code: %s", url, response.status_code)

            self.send_response(response.status_code)

            content_type = response.headers.get("Content-Type", "application/octet-stream")
            self.send_header("Content-Type", content_type)

            if "Content-Length" in response.headers:
                self.send_header("Content-Length", response.headers["Content-Length"])

            self.end_headers()

            if response.content:
                self.wfile.write(response.content)

        except requests.exceptions.Timeout:
            logging.error("Timeout while requesting %s", url)
            self.send_response(504)
            self.end_headers()
            self.wfile.write(b"Gateway Timeout")

        except requests.exceptions.RequestException as e:
            logging.error("Error while requesting %s: %s", url, e)
            self.send_response(502)
            self.end_headers()
            self.wfile.write(b"Bad Gateway")


def run(port=8888):
    server_address = ("", port)
    httpd = http.server.HTTPServer(server_address, Proxy)
    print(f"Proxy server started at http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()