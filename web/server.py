from flask import Flask, render_template_string, request
import qrcode
import io
import base64

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>⚡ LinkQR ⚡</title>
  <link rel="stylesheet" href="/style.css" />
</head>
<body>
  <div class="container">
    <h1>⚡ LinkQR ⚡</h1>
    <p class="tagline">Turn any link into a glowing neon QR code</p>

    <div class="form">
      <form method="POST">
        <input type="text" name="url" placeholder="https://example.com" required />
        <button type="submit">Generate QR</button>
      </form>
    </div>

    <div class="qr-display">
      {% if qr_code %}
        <img src="data:image/png;base64,{{ qr_code }}" alt="QR Code" style="box-shadow:0 0 20px #0ff; border-radius:10px;">
      {% else %}
        <p>No QR yet. Submit a link above to generate one.</p>
      {% endif %}
    </div>

    <footer>
      <p>Made by <strong>Anonymous</strong> • <span class="brand">LinkQR</span> — Open Source</p>
    </footer>
  </div>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def index():
    qr_code = None
    if request.method == "POST":
        url = request.form["url"]
        qr = qrcode.QRCode(box_size=8, border=2)
        qr.add_data(url)
        qr.make(fit=True)
        img = qr.make_image(fill_color="cyan", back_color="black")

        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        qr_code = base64.b64encode(buffer.getvalue()).decode()

    return render_template_string(HTML_TEMPLATE, qr_code=qr_code)

@app.route("/style.css")
def style():
    css = open("web/style.css").read()
    return app.response_class(css, mimetype="text/css")

if __name__ == "__main__":
    print("🚀 Serving neon LinkQR preview on http://127.0.0.1:8000")
    app.run(host="127.0.0.1", port=8000)
