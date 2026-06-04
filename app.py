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
                'Cookie': 'AWSALBTG=x7mzbr8Nr67JyIFgalxjhFsm5355q1Bd1/tNVtcbyAdMYUHGoWKLpdoh46oNfFeqUyJg+pVL8aCO9tSavYM6iWBF8SmZYm/FSPO+UGOpBuL39q671OoDkALPLLlo8Ttpo7slK0140m0Hh7Nf+yZPtm5e4ks1Rk2dlX2L+Qyx+QVVtBDzRfg=; AWSALBTGCORS=x7mzbr8Nr67JyIFgalxjhFsm5355q1Bd1/tNVtcbyAdMYUHGoWKLpdoh46oNfFeqUyJg+pVL8aCO9tSavYM6iWBF8SmZYm/FSPO+UGOpBuL39q671OoDkALPLLlo8Ttpo7slK0140m0Hh7Nf+yZPtm5e4ks1Rk2dlX2L+Qyx+QVVtBDzRfg=; AWSALB=yyWq7MzXfCuMzMZFamEtGBA4TzthxCecxnlBShysI1/NWJoj1D9g1x2oxk0mqyrf1L32yLLVWdP6UEJxIZWeAAhsvCZKjaoGP1LVxXPi9ebkSitgJYOmevFuDujc; AWSALBCORS=yyWq7MzXfCuMzMZFamEtGBA4TzthxCecxnlBShysI1/NWJoj1D9g1x2oxk0mqyrf1L32yLLVWdP6UEJxIZWeAAhsvCZKjaoGP1LVxXPi9ebkSitgJYOmevFuDujc'
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
