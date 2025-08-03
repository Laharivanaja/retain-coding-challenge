from flask import Flask, request, jsonify, redirect
import random
import string
from urllib.parse import urlparse

app = Flask(__name__)

# In-memory store
url_map = {}  # short_code -> { original_url, hits }

def generate_short_code(length=6):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def is_valid_url(url):
    try:
        parsed = urlparse(url)
        return parsed.scheme in ('http', 'https') and parsed.netloc != ''
    except:
        return False

@app.route('/')
def home():
    return "Welcome to the Flask URL Shortener!"

@app.route('/shorten', methods=['POST'])
def shorten_url():
    data = request.get_json()
    if not data or 'url' not in data:
        return jsonify({'error': 'URL is required'}), 400

    original_url = data['url']
    if not is_valid_url(original_url):
        return jsonify({'error': 'Invalid URL'}), 400

    short_code = generate_short_code()
    while short_code in url_map:
        short_code = generate_short_code()

    url_map[short_code] = {'original_url': original_url, 'hits': 0}
    short_url = request.host_url + short_code
    return jsonify({'shortened_url': short_url}), 201

@app.route('/<short_code>')
def redirect_to_original(short_code):
    entry = url_map.get(short_code)
    if not entry:
        return jsonify({'error': 'Short URL not found'}), 404

    entry['hits'] += 1
    return redirect(entry['original_url'])

@app.route('/stats/<short_code>')
def get_stats(short_code):
    entry = url_map.get(short_code)
    if not entry:
        return jsonify({'error': 'Short URL not found'}), 404

    return jsonify({
        'original_url': entry['original_url'],
        'hits': entry['hits']
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5009, debug=True)
