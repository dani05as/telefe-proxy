from flask import Flask, jsonify
import requests
import threading
import time

TELEGRAM_TOKEN = '8623468208:AAF63NWKDZTHVuOK01yT0GPrzG8pwg21ewA'
TELEGRAM_CHAT_ID = '8750567244'

def enviar_telegram(mensaje):
    try:
        requests.get(
            f'https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage',
            params={'chat_id': TELEGRAM_CHAT_ID, 'text': mensaje}
        )
    except:
        pass

app = Flask(__name__)

def keep_alive():
    while True:
        try:
            requests.get('https://telefe-proxy.onrender.com/stream')
            print("Ping enviado")
        except:
            pass
        time.sleep(600)

thread = threading.Thread(target=keep_alive)
thread.daemon = True
thread.start()

@app.route('/stream')
def get_stream():
    try:
        response = requests.post(
            'https://mitelefe.com/vidya/tokenize',
            json={"url": "https://telefeappmitelefe1.akamaized.net/hls/live/2037985/appmitelefe/TOK/master.m3u8"},
            headers={
                'Origin': 'https://mitelefe.com',
                'Referer': 'https://mitelefe.com/telefe-en-vivo',
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
                'Content-Type': 'application/json',
                'Accept': '*/*',
                'Cookie': 'AWSALBTG=wjj1MRXq66+MIqLv4iWZ+fn899nW9JX1Oo2bGRpvshb0N9CdYCRpB4gx+xTiSUiJ5tUQTUgdBCWKFX3By45M+tmcEht4kKRdaGhWpCWwXfTAfLFdS0yPL+XgmDdBvpBo8fmywBbkVa+n5B7BFkel9Y1PkN1zEP6zgybhPrB9QtLL/zGfxYU=; AWSALBTGCORS=wjj1MRXq66+MIqLv4iWZ+fn899nW9JX1Oo2bGRpvshb0N9CdYCRpB4gx+xTiSUiJ5tUQTUgdBCWKFX3By45M+tmcEht4kKRdaGhWpCWwXfTAfLFdS0yPL+XgmDdBvpBo8fmywBbkVa+n5B7BFkel9Y1PkN1zEP6zgybhPrB9QtLL/zGfxYU=; AWSALB=PPC6BlQmeyqbBnESHph9oIFLyaZBopr4HeYUeJltQZoEYIBFWtFQgrM9pqed/+N+4nBKow1NF0yUkqSRXMiWjG3hz87MClr2btEcvH05O/fnJEI3K4Rf9RWTSHk/; AWSALBCORS=PPC6BlQmeyqbBnESHph9oIFLyaZBopr4HeYUeJltQZoEYIBFWtFQgrM9pqed/+N+4nBKow1NF0yUkqSRXMiWjG3hz87MClr2btEcvH05O/fnJEI3K4Rf9RWTSHk/'
            },
            timeout=10
        )
        data = response.json()
        url = data.get('url')
        if url:
            return jsonify({"stream_url": url})
        enviar_telegram('⚠️ Mi Canal TV: Las cookies expiraron, hay que actualizarlas.')
        return jsonify({"error": "Stream no disponible"}), 503
    except Exception as e:
        enviar_telegram(f'⚠️ Mi Canal TV: Error en el servidor: {str(e)}')
        return jsonify({"error": str(e)}), 503
