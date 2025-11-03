from http.server import SimpleHTTPRequestHandler, HTTPServer
import os

PORT = 8000
WEB_DIR = os.path.join(os.getcwd(), "web")

class QRHandler(SimpleHTTPRequestHandler):
    def translate_path(self, path):
        path = SimpleHTTPRequestHandler.translate_path(self, path)
        relpath = os.path.relpath(path, os.getcwd())
        full_path = os.path.join(WEB_DIR, relpath)
        return full_path

if __name__ == "__main__":
    os.chdir(WEB_DIR)
    print(f"🚀 Neon Web Preview running at http://127.0.0.1:{PORT}")
    print("Press CTRL+C to stop.")
    with HTTPServer(("0.0.0.0", PORT), QRHandler) as httpd:
        httpd.serve_forever()
