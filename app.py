from flask import Flask, jsonify
import requests
import threading
import time

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

app = Flask(__name__)

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
        print(f"Status: {response.status_code}")
        print(f"Response: {response.text}")
        data = response.json()
        url = data.get('url')
        if url:
            return jsonify({"stream_url": url})
        return jsonify({"error": "No url en respuesta", "data": data}), 503
    except Exception as e:
        print(f"Error: {e}")
        return jsonify({"error": str(e)}), 503