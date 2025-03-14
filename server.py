from http.server import SimpleHTTPRequestHandler, HTTPServer

class CORSRequestHandler(SimpleHTTPRequestHandler):
    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        super().end_headers()

PORT = 8000
server_address = ("", PORT)
httpd = HTTPServer(server_address, CORSRequestHandler)

print(f"Serving at http://127.0.0.1:{PORT}")
httpd.serve_forever()
