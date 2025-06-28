from flask import Flask
from requests import request

app = Flask(__name__)

@app.get('/')
def index():
  return '<h1>Hello World</h1>'



if __name__ == '__main__':
  app.run(debug=True, host='0.0.0.0', port=5851)