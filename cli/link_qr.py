from time import sleep
from rich.console import Console
from rich.text import Text
from rich.live import Live

console = Console()

def neon_ascii_banner():
    frames = [
        "[bright_cyan]██╗     ██╗██╗███╗   ██╗ ██████╗ ██╗██████╗[/bright_cyan]",
        "[cyan]██║     ██║██║████╗  ██║██╔═══██╗██║██╔══██╗[/cyan]",
        "[bright_cyan]██║ █╗  ██║██║██╔██╗ ██║██║   ██║██║██║  ██║[/bright_cyan]",
        "[cyan]██║███╗ ██║██║██║╚██╗██║██║   ██║██║██║  ██║[/cyan]",
        "[bright_cyan]╚███╔███╔╝██║██║ ╚████║╚██████╔╝██║██████╔╝[/bright_cyan]",
        "[cyan] ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝ ╚═════╝ ╚═╝╚═════╝[/cyan]",
        "\n[yellow]⚡ LinkQR v1.0.0 | Ethical Neon QR Generator ⚡[/yellow]"
    ]

    with Live(console=console, refresh_per_second=8) as live:
        for _ in range(2):  # loop animation twice
            for frame in frames:
                live.update(Text(frame, justify="center"))
                sleep(0.2)
#!/usr/bin/env python3
"""
Link QR CLI — generate QR and optionally show a neon web preview.

Usage:
  python cli/link_qr.py "https://example.com" --out myqr.png
  python cli/link_qr.py "example.com" --web         # generate and open local neon page
"""


import os
import subprocess
import qrcode

def generate_qr(link, outfile=None):
    qr = qrcode.QRCode(box_size=8, border=2)
    qr.add_data(link)
    qr.make(fit=True)
    img = qr.make_image(fill_color="cyan", back_color="black")

    if outfile:
        img.save(outfile)
        print(f"[✅] QR saved to: {outfile}")
    else:
        print("[⚡] QR generated successfully (not saved).")

def main():
    link = input("Enter your link: ").strip()
    if not link:
        print("❌ Please enter a valid link.")
        return

    out_path = "web/generated.png"
    generate_qr(link, out_path)

    print("[🌐] Launching neon web preview...")
    subprocess.Popen(["python3", "web/server.py"])
    os.system("termux-open-url http://127.0.0.1:8000")
if __name__ == "__main__":
    main()
