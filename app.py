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
