from flask import Flask, jsonify
import requests
import threading
import time
import os

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")
MITELEFE_COOKIE = os.getenv("MITELEFE_COOKIE")

app = Flask(__name__)

def enviar_telegram(mensaje):
    if not TELEGRAM_TOKEN or not TELEGRAM_CHAT_ID:
        return
    try:
        requests.get(
            f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage",
            params={"chat_id": TELEGRAM_CHAT_ID, "text": mensaje},
            timeout=10
        )
    except:
        pass

def keep_alive():
    while True:
        try:
            requests.get("https://telefe-proxy.onrender.com/stream", timeout=10)
            print("Ping enviado")
        except:
            pass
        time.sleep(600)

thread = threading.Thread(target=keep_alive)
thread.daemon = True
thread.start()

@app.route("/stream")
def get_stream():
    try:
        response = requests.post(
            "https://mitelefe.com/vidya/tokenize",
            json={"url": "https://telefeappmitelefe1.akamaized.net/hls/live/2037985/appmitelefe/TOK/master.m3u8"},
            headers={
                "Origin": "https://mitelefe.com",
                "Referer": "https://mitelefe.com/telefe-en-vivo",
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36",
                "Content-Type": "application/json",
                "Accept": "*/*",
                "Cookie": MITELEFE_COOKIE
            },
            timeout=10
        )
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        data = response.json()
        url = data.get("url")
        if url:
            return jsonify({"stream_url": url})
        enviar_telegram("⚠️ Mi Canal TV: Las cookies expiraron.")
        return jsonify({"error": "Stream no disponible"}), 503
    except Exception as e:
        enviar_telegram(f"⚠️ Mi Canal TV: Error: {str(e)}")
        return jsonify({"error": str(e)}), 503
