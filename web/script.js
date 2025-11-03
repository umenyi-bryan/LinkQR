document.getElementById('generateBtn').addEventListener('click', () => {
  const url = document.getElementById('urlInput').value.trim();
  const qrDisplay = document.getElementById('qrDisplay');

  if (!url) {
    qrDisplay.innerHTML = '<p style="color:#ff4d4d;">Please enter a valid URL.</p>';
    return;
  }

  const qrApi = `https://api.qrserver.com/v1/create-qr-code/?data=${encodeURIComponent(url)}&size=200x200`;

  qrDisplay.innerHTML = `<img src="${qrApi}" alt="QR Code" style="box-shadow:0 0 20px #0ff; border-radius:10px;">`;
});
