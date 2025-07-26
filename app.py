from flask import Flask, request, jsonify, send_file
import requests, os

app = Flask(__name__)

DOWNLOAD_FOLDER = 'downloads'
if not os.path.exists(DOWNLOAD_FOLDER):
    os.makedirs(DOWNLOAD_FOLDER)

@app.route('/')
def index():
    return '''
    <html>
    <head><title>Cloud Downloader</title></head>
    <body>
    <h2>☁️ Cloud Downloader Ready</h2>
    <form onsubmit="return false;">
        <input type="text" id="url" placeholder="Enter download URL" style="width:80%;padding:10px;"><br><br>
        <button onclick="download()">Download via Cloud</button>
    </form>
    <div id="result" style="margin-top:20px;"></div>

    <script>
        async function download() {
            const url = document.getElementById('url').value;
            const res = await fetch('/download', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({url: url})
            });
            const data = await res.json();
            const filename = data.file.split('/').pop();
            document.getElementById('result').innerHTML = 
              '<a href="/get?filename=' + filename + '" download>⬇️ Click here to download: ' + filename + '</a>';
        }
    </script>
    </body>
    </html>
    '''

@app.route('/download', methods=['POST'])
def download_file():
    url = request.json.get("url")
    filename = url.split("/")[-1]
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)

    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(filepath, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        return jsonify({"file": filepath})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/get', methods=['GET'])
def get_file():
    filename = request.args.get("filename")
    filepath = os.path.join(DOWNLOAD_FOLDER, filename)
    return send_file(filepath, as_attachment=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
