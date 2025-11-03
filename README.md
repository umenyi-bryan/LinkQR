![GitHub stars](https://img.shields.io/github/stars/umenyi-bryan/link-qr?style=for-the-badge)
![GitHub forks](https://img.shields.io/github/forks/umenyi-bryan/link-qr?style=for-the-badge)
![GitHub license](https://img.shields.io/github/license/umenyi-bryan/link-qr?style=for-the-badge)
![Python version](https://img.shields.io/badge/python-3.10+-blue?style=for-the-badge)
# ⚡ LinkQR ⚡

Turn any link into a glowing neon QR code.

![Preview](https://raw.githubusercontent.com/umenyi-bryan/link-qr/main/web/generated.png)

---

## 🌐 Features
- Convert any URL into a QR code.
- View it instantly on a neon-styled local web page.
- Works on **Termux**, **Kali Linux**, and **Windows**.
- Open source and extendable.

---

## 🚀 Quick Start

```bash
# Clone the repo
git clone https://github.com/umenyi-bryan/link-qr.git
cd link-qr

# Set up environment
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt

# Run it
python3 cli/link_qr.py

# Then open the glowing web preview at
http://127.0.0.1:8000

link-qr/
├── cli/           # Command-line interface
├── web/           # Flask neon web preview
├── requirements.txt
└── README.md

🛠 Made by Anonymous

Open source • MIT License

