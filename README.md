# 🌐 LinkQR

Turn any link into a stunning neon QR code — cross-platform for Termux, Kali Linux, and Windows.

## ✨ Features
- Generate QR codes from any URL
- Neon-styled local web preview
- Simple CLI (Command Line Interface)
- Lightweight and portable
- Open source and easy to modify

---

## ⚙️ Quick Start

### 1. Clone the repository
```bash
git clone https://github.com/umenyi-bryan/LinkQR.git
cd LinkQR
python3 -m venv venv
source venv/bin/activate   # On Termux/Linux
# OR
venv\Scripts\activate      # On Windows
pip install -r requirements.txt
python3 cli/link_qr.py "https://example.com" --out ./out/example.png --neon
python3 web_preview.py
http://127.0.0.1:8000

LinkQR/
│
├── cli/
│   └── link_qr.py        # Main CLI entry point
│
├── web/
│   ├── index.html        # Neon QR web interface
│   ├── style.css         # Neon theme styling
│   └── script.js         # Dynamic QR display
│
├── out/                  # Generated QR codes
├── requirements.txt      # Python dependencies
└── README.md             # This file
