from flask import Flask, request, redirect
import yt_dlp

app = Flask(__name__)

CHANNELS = {
    "sozcu": "https://www.youtube.com/@SozcuTelevizyonu/live",
    "cnnturk": "https://www.youtube.com/@cnnturk/live",
    "haberturk": "https://www.youtube.com/@HaberturkTV/live",
    "ntv": "https://www.youtube.com/@ntv/live"
}

def get_direct_url(youtube_url):
    ydl_opts = {'format': 'best', 'quiet': True, 'simulate': True}
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(youtube_url, download=False).get('url')
    except:
        return None

@app.route('/')
def proxy():
    kanal = request.args.get('kanal', 'sozcu').lower()
    if kanal not in CHANNELS:
        return "Kanal bulunamadi.", 404
    
    url = get_direct_url(CHANNELS[kanal])
    if url:
        return redirect(url, code=302)
    return "Yayin alinamadi.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
