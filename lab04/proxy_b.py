import http.server
import logging
import requests
import os
import json
import hashlib

logging.basicConfig(
    filename="proxy.log",
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s"
)

CACHE_DIR = "cache"
os.makedirs(CACHE_DIR, exist_ok=True)

BLACKLIST_FILE = "blacklist.txt"
def load_blacklist():
    try:
        with open(BLACKLIST_FILE, "r") as f:
            return [line.strip() for line in f if line.strip()]
    except FileNotFoundError:
        return []

BLACKLIST = load_blacklist()
def is_blocked(url):
    for blocked in BLACKLIST:
        if blocked in url:
            return True
    return False


def get_cache_key(url):
    return hashlib.md5(url.encode()).hexdigest()


def get_cache_paths(url):
    key = get_cache_key(url)
    return (
        os.path.join(CACHE_DIR, key + ".body"),
        os.path.join(CACHE_DIR, key + ".meta")
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
        if is_blocked(url):
            logging.info("BLOCKED URL: %s", url)
            self.send_response(403)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Access denied: URL is blocked by proxy")
            return

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
                body_path, meta_path = get_cache_paths(url)

                if os.path.exists(body_path) and os.path.exists(meta_path):
                    with open(meta_path, "r", encoding="utf-8") as f:
                        meta = json.load(f)

                    if meta.get("etag"):
                        forward_headers["If-None-Match"] = meta["etag"]
                    if meta.get("last_modified"):
                        forward_headers["If-Modified-Since"] = meta["last_modified"]

                    response = requests.get(url, headers=forward_headers, timeout=10)

                    if response.status_code == 304:
                        with open(body_path, "rb") as f:
                            cached_body = f.read()

                        logging.info("URL: %s, Response Code: %s, Cache: HIT", url, 200)

                        self.send_response(200)
                        self.send_header(
                            "Content-Type",
                            meta.get("content_type", "application/octet-stream")
                        )
                        self.send_header("Content-Length", str(len(cached_body)))
                        self.end_headers()
                        self.wfile.write(cached_body)
                        return

                else:
                    response = requests.get(url, headers=forward_headers, timeout=10)

                logging.info("URL: %s, Response Code: %s, Cache: MISS", url, response.status_code)

                self.send_response(response.status_code)

                content_type = response.headers.get("Content-Type", "application/octet-stream")
                self.send_header("Content-Type", content_type)

                if "Content-Length" in response.headers:
                    self.send_header("Content-Length", response.headers["Content-Length"])
                else:
                    self.send_header("Content-Length", str(len(response.content)))

                self.end_headers()

                if response.content:
                    self.wfile.write(response.content)

                if response.status_code == 200:
                    with open(body_path, "wb") as f:
                        f.write(response.content)

                    with open(meta_path, "w", encoding="utf-8") as f:
                        json.dump({
                            "etag": response.headers.get("ETag"),
                            "last_modified": response.headers.get("Last-Modified"),
                            "content_type": content_type
                        }, f)

            else:
                response = requests.post(url, headers=forward_headers, data=body, timeout=10)

                logging.info("URL: %s, Response Code: %s", url, response.status_code)

                self.send_response(response.status_code)

                content_type = response.headers.get("Content-Type", "application/octet-stream")
                self.send_header("Content-Type", content_type)

                if "Content-Length" in response.headers:
                    self.send_header("Content-Length", response.headers["Content-Length"])
                else:
                    self.send_header("Content-Length", str(len(response.content)))

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
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, Proxy)
    print(f"Proxy server started at http://localhost:{port}")
    httpd.serve_forever()


if __name__ == "__main__":
    run()