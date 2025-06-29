import os
from flask import Flask, request, jsonify
import requests

API_URL = "api.open-meteo.com/v1/forecast"

app = Flask(__name__)

@app.get('/')
def index():
    return '<h1>Hello World</h1>'

@app.get('/health')
def health():
    return {'status': 'healthy'}, 200


@app.get('/weather')
def get_weather():
    lat = request.args.get('latitude')
    long = request.args.get('longitude')
    url = f"https://{API_URL}?latitude={lat}&longitude={long}"
    response = requests.request(url)
    data = response.json()

    return jsonify(data)

if __name__ == '__main__':
  # Use environment variables for configuration
    debug = os.getenv('FLASK_ENV') == 'development'
    host = os.getenv('FLASK_HOST', '0.0.0.0')
    port = os.getenv('FLASK_PORT', '5851')
  
    app.run(debug=debug, host=host, port=port)
