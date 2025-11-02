#!/usr/bin/env python3
"""
Link QR CLI — generate QR and optionally show a neon web preview.

Usage:
  python cli/link_qr.py "https://example.com" --out myqr.png
  python cli/link_qr.py "example.com" --web         # generate and open local neon page
"""

from __future__ import annotations
import argparse
import os
import sys
import tempfile
import threading
import socket
import webbrowser
from pathlib import Path

# --- imports that are required ---
try:
    import qrcode
    from qrcode.constants import ERROR_CORRECT_H
    from PIL import Image
    import requests
    import pyfiglet
    from colorama import init as _cinit, Fore, Style
    from flask import Flask, render_template, send_from_directory
except Exception as e:
    print("Missing dependencies or running first-time install. Install requirements with:")
    print("  pip install -r requirements.txt")
    print("Error detail:", e)
    sys.exit(1)

_cinit()  # colorama init

ROOT = Path(__file__).resolve().parents[1]  # project root (one level above cli/)
WEB_DIR = ROOT / "web"
WEB_STATIC = WEB_DIR / "static"
WEB_TEMPLATES = WEB_DIR / "templates"

DEFAULT_OUT = "link_qr.png"

# -----------------------
# Utilities
# -----------------------
def ensure_http(url: str) -> str:
    url = url.strip()
    if url.startswith("http://") or url.startswith("https://"):
        return url
    return "https://" + url

def local_ip() -> str:
    """Best-effort local IP (for sharing across LAN)."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
    except Exception:
        ip = "127.0.0.1"
    finally:
        s.close()
    return ip

def short_tinyurl(url: str) -> str | None:
    try:
        r = requests.get("https://tinyurl.com/api-create.php", params={"url": url}, timeout=6)
        if r.status_code == 200:
            return r.text.strip()
    except Exception:
        return None
    return None

# -----------------------
# QR generation
# -----------------------
def generate_qr_image(data: str, out_path: str, box_size: int = 8, border: int = 4, fg: str = "black", bg: str = "white"):
    qr = qrcode.QRCode(version=1,
                       error_correction=ERROR_CORRECT_H,
                       box_size=box_size,
                       border=border)
    qr.add_data(data)
    qr.make(fit=True)
    img = qr.make_image(fill_color=fg, back_color=bg).convert("RGB")
    img.save(out_path)
    return out_path

# -----------------------
# Web preview (Flask)
# -----------------------
def run_flask_server(serve_dir: str, port: int = 5000, open_browser: bool = True):
    app = Flask("linkqr_preview", template_folder=str(WEB_TEMPLATES), static_folder=str(WEB_STATIC))

    @app.route("/")
    def index():
        # discover the most recent qrcode in serve_dir (by mtime)
        serve_dir_path = Path(serve_dir)
        pngs = sorted(serve_dir_path.glob("*.png"), key=lambda p: p.stat().st_mtime, reverse=True)
        chosen = pngs[0].name if pngs else None
        return render_template("index.html", qrcode_filename=chosen, link_text=None)

    @app.route("/qrcode/<path:filename>")
    def qrcode_file(filename):
        return send_from_directory(serve_dir, filename)

    def _run():
        # bind to 0.0.0.0 so other devices on the LAN can reach it if needed
        app.run(host="0.0.0.0", port=port, debug=False, use_reloader=False)

    t = threading.Thread(target=_run, daemon=True)
    t.start()

    host = local_ip()
    url = f"http://{host}:{port}/"
    if open_browser:
        try:
            webbrowser.open(url)
        except Exception:
            print(f"[+] Preview available at {url}")
    print(f"[+] Preview server running at {url} (press Ctrl-C to stop)")
    return t, url

# -----------------------
# Pretty banner
# -----------------------
def show_banner(title: str = "Link QR"):
    try:
        banner = pyfiglet.figlet_format(title, font="slant")
    except Exception:
        banner = title + "\n"
    print(Fore.CYAN + banner + Style.RESET_ALL)
    print(Fore.MAGENTA + "  ⚡ Convert any link into a scan-ready QR — neon web preview included ⚡\n" + Style.RESET_ALL)

# -----------------------
# CLI
# -----------------------
def parse_args():
    p = argparse.ArgumentParser(prog="link_qr",
                                description="Generate QR codes and optionally show a neon web preview.")
    p.add_argument("link", help="Link or text to encode")
    p.add_argument("--out", "-o", help="Output PNG path (default: link_qr.png)", default=DEFAULT_OUT)
    p.add_argument("--web", action="store_true", help="Start a neon web preview (opens browser)")
    p.add_argument("--port", type=int, default=5000, help="Port for web preview (default 5000)")
    p.add_argument("--shorten", action="store_true", help="Attempt to shorten the URL via TinyURL before encoding")
    return p.parse_args()

def main():
    args = parse_args()
    show_banner("Link QR")

    link = ensure_http(args.link)
    if args.shorten:
        s = short_tinyurl(link)
        if s:
            print(f"[+] Shortened link -> {s}")
            link = s
        else:
            print("[!] Shorten failed; continuing with original link.")

    out_path = Path(args.out).expanduser().resolve()
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # Generate QR
    try:
        generate_qr_image(link, str(out_path))
        print(Fore.GREEN + f"[+] Saved QR PNG: {out_path}" + Style.RESET_ALL)
    except Exception as e:
        print("[!] Failed to generate QR:", e)
        sys.exit(2)

    # If --web: copy the image into the web folder (WEB_DIR) so Flask can serve it,
    # or simply serve from the out_path.parent; for simplicity we'll serve from out_path.parent
    if args.web:
        serve_dir = str(out_path.parent)
        t, url = run_flask_server(serve_dir, port=args.port, open_browser=True)
        try:
            # block until CTRL+C
            while True:
                t.join(1)
        except KeyboardInterrupt:
            print("\n[!] Stopping preview server. Bye.")
            sys.exit(0)

if __name__ == "__main__":
    main()
