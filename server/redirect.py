from flask import Flask, redirect, request, jsonify
from datetime import datetime
import os, json, hashlib

app = Flask(__name__)
DATA_FILE = os.environ.get('LR_DATA_FILE', 'clicks.json')

# tiny in-memory map; in production store in a DB
MAP = {
    'ex1': 'https://example.com'
}

def record(shortcode):
    entry = {
        'time': datetime.utcnow().isoformat()+'Z',
        'short': shortcode,
        'ua': request.headers.get('User-Agent','-'),
        # omit raw IP by default — store a hashed token instead
        'ip_hash': hashlib.sha256(request.remote_addr.encode()).hexdigest()[:16] if request.remote_addr else None
    }
    try:
        a=[]
        if os.path.exists(DATA_FILE):
            a=json.load(open(DATA_FILE))
        a.append(entry)
        json.dump(a, open(DATA_FILE,'w'), indent=2)
    except Exception:
        pass

@app.route('/<code>')
def r(code):
    if code in MAP:
        record(code)
        return redirect(MAP[code])
    return 'Not found', 404

@app.route('/map', methods=['GET','POST'])
def map_view():
    if request.method=='GET':
        return jsonify(MAP)
    data = request.get_json() or {}
    key = data.get('key')
    url = data.get('url')
    if not key or not url:
        return 'bad', 400
    MAP[key]=url
    return 'ok'

if __name__=='__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
