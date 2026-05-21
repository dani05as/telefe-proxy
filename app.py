from flask import Flask, jsonify
import requests
import threading
import time

app = Flask(__name__)
stream_url = None

def renovar_token():
    global stream_url
    while True:
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
                }
            )
            data = response.json()
            stream_url = data.get('url')
            print(f"Token renovado: {stream_url}")
        except Exception as e:
            print(f"Error renovando token: {e}")
        time.sleep(1800)

@app.route('/stream')
def get_stream():
    if stream_url:
        return jsonify({"stream_url": stream_url})
    return jsonify({"error": "Stream no disponible"}), 503

if __name__ == '__main__':
    thread = threading.Thread(target=renovar_token)
    thread.daemon = True
    thread.start()
    renovar_token()
    app.run(host='0.0.0.0', port=5000)