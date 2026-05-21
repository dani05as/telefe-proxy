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
                'Cookie': 'AWSALBTG=JEfqXUW4NpTRWlKZEt+HrPk106t2heNXR6BQFu+5ebKZIvUPAG9KgAIb8ofX1M9tbTd920jEOuox+U8WyhmCgOYJlLQwqjYFTshVihBVaw9MFTuVYU7g1lNUH7C7iQe4kB2xwRaAVRGlyhy9x5xRHBpHaFPbX/Cdn+VgjpVji8IxhepLRMY=; AWSALBTGCORS=JEfqXUW4NpTRWlKZEt+HrPk106t2heNXR6BQFu+5ebKZIvUPAG9KgAIb8ofX1M9tbTd920jEOuox+U8WyhmCgOYJlLQwqjYFTshVihBVaw9MFTuVYU7g1lNUH7C7iQe4kB2xwRaAVRGlyhy9x5xRHBpHaFPbX/Cdn+VgjpVji8IxhepLRMY=; AWSALB=o98QJYNu01MD6XwHugXEpgBDPoRlc1jcG6k/1VbXjIvXsuUPY7OYGXXK7VxLl9y8z53kxgyTLAvv0f8F05duaFLFpCb36dyyMJrAHSNngmdr0pJXjdqX9TDUs8kA; AWSALBCORS=o98QJYNu01MD6XwHugXEpgBDPoRlc1jcG6k/1VbXjIvXsuUPY7OYGXXK7VxLl9y8z53kxgyTLAvv0f8F05duaFLFpCb36dyyMJrAHSNngmdr0pJXjdqX9TDUs8kA'
            },
            timeout=10
        )
        data = response.json()
        url = data.get('url')
        if url:
            return jsonify({"stream_url": url})
        enviar_telegram('⚠️ Telefe TV: Las cookies expiraron, hay que actualizarlas.')
        return jsonify({"error": "Stream no disponible"}), 503
    except Exception as e:
        enviar_telegram(f'⚠️ Telefe TV: Error en el servidor: {str(e)}')
        return jsonify({"error": str(e)}), 503
