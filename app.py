from flask import Flask, request, redirect
import yt_dlp

app = Flask(__name__)

# Kanal kütüphanemiz
CHANNELS = {
    "sozcu": "https://www.youtube.com/@SozcuTelevizyonu/live",
    "cnnturk": "https://www.youtube.com/@cnnturk/live",
    "haberturk": "https://www.youtube.com/@HaberturkTV/live",
    "ntv": "https://www.youtube.com/@ntv/live"
}

def get_direct_url(youtube_url):
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'simulate': True,
        # İŞTE YENİ SİLAHIMIZ: Çerez dosyasını okuma komutu
        'cookiefile': 'cookies.txt',
        'extractor_args': {'youtube': ['player_client=android,web']}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            return ydl.extract_info(youtube_url, download=False).get('url')
    except Exception as e:
        print(f"Hata detayı: {e}")
        return None

@app.route('/')
def proxy():
    kanal = request.args.get('kanal', 'sozcu').lower()
    if kanal not in CHANNELS:
        return "Kanal listemizde bulunamadi.", 404
    
    direct_url = get_direct_url(CHANNELS[kanal])
    if direct_url:
        return redirect(direct_url, code=302)
    
    return "Yayin alinamadi. Cerezler gecersiz olabilir veya YouTube sunucuyu engelledi.", 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
