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
                'Cookie': 'AWSALBTG=ETT4l6FeuuMw7IDqbXTRp04XCy9fnwhU3y8fwzFVBYmAtDXgx1vGRpUuX81ZT2YCKC72oNlhBm0rgijy/EP1iJUqymV7WvWWX3FQ9LJitCXVBIP42FXq9BDbBFHPZA8ae2NR2QaZ397e71wdv3v7BkBAy/g5TK9ExppIi6hEMK1k8oRANRk=; AWSALBTGCORS=ETT4l6FeuuMw7IDqbXTRp04XCy9fnwhU3y8fwzFVBYmAtDXgx1vGRpUuX81ZT2YCKC72oNlhBm0rgijy/EP1iJUqymV7WvWWX3FQ9LJitCXVBIP42FXq9BDbBFHPZA8ae2NR2QaZ397e71wdv3v7BkBAy/g5TK9ExppIi6hEMK1k8oRANRk=; AWSALB=kWYEaAoyQbDiNzT/mn7onHn7iS5oQBNvHkj/imhPXH/iiPu6wCI4UelLW87T/UPDH38KC9rJQrjGWkufvNQyGT1gCk4vjRoh6GYNp8eOMpB67rIBewUFlyk+R5+3; AWSALBCORS=kWYEaAoyQbDiNzT/mn7onHn7iS5oQBNvHkj/imhPXH/iiPu6wCI4UelLW87T/UPDH38KC9rJQrjGWkufvNQyGT1gCk4vjRoh6GYNp8eOMpB67rIBewUFlyk+R5+3'
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
