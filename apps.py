# app.py
from flask import Flask, request, jsonify, send_file
import requests, os
from urllib.parse import quote
from pytube import YouTube

app = Flask(__name__)
DOWNLOAD_PATH = "downloads"

if not os.path.exists(DOWNLOAD_PATH):
    os.makedirs(DOWNLOAD_PATH)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get("q")
    return jsonify({
        "result": f"https://www.google.com/search?q={quote(query)}"
    })

@app.route('/download', methods=['POST'])
def download():
    url = request.json.get("url")
    if "youtube.com" in url:
        yt = YouTube(url)
        stream = yt.streams.filter(progressive=True, file_extension='mp4').first()
        out_file = stream.download(output_path=DOWNLOAD_PATH)
        return jsonify({"file": out_file})
    else:
        local_filename = os.path.join(DOWNLOAD_PATH, url.split("/")[-1])
        with requests.get(url, stream=True) as r:
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return jsonify({"file": local_filename})

@app.route('/get', methods=['GET'])
def get_file():
    filename = request.args.get("filename")
    filepath = os.path.join(DOWNLOAD_PATH, filename)
    return send_file(filepath, as_attachment=True)

app.run(host='0.0.0.0', port=5000)
