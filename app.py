from flask import Flask, render_template, request, send_from_directory, redirect, url_for
import qrcode
import os

# Use 'web' as the template/static folder so your CSS and template live in web/
app = Flask(__name__, template_folder="web", static_folder="web")

# Directory where generated QR PNGs will be written and served from
OUT_DIR = os.path.join(app.static_folder, "out")
os.makedirs(OUT_DIR, exist_ok=True)
LATEST_FILENAME = "latest.png"

@app.route("/", methods=("GET", "POST"))
def index():
    qrcode_path = None
    if request.method == "POST":
        url = request.form.get("url", "").strip()
        if url:
            # generate QR and save into web/out/latest.png so it's served as /out/latest.png
            img = qrcode.make(url)
            save_path = os.path.join(OUT_DIR, LATEST_FILENAME)
            img.save(save_path)
            return redirect(url_for("index"))  # avoid form resubmit; show generated image
    # if file exists, show it
    candidate = os.path.join(OUT_DIR, LATEST_FILENAME)
    if os.path.exists(candidate):
        qrcode_path = f"out/{LATEST_FILENAME}"
    return render_template("index.html", qrcode_filename=qrcode_path)

# Optional route to download (if you want to force attachment)
@app.route("/download")
def download():
    return send_from_directory(OUT_DIR, LATEST_FILENAME, as_attachment=True)

if __name__ == "__main__":
    # debug=True OK for development; set debug=False before public exposure
    app.run(host="0.0.0.0", port=8000, debug=True)
