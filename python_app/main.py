from flask import Flask, render_template
import requests

app = Flask(__name__)

@app.route('/')
def get_public_ip():
    # Get the public IP from api
    response = requests.get('https://api.ipify.org?format=json')
    ip = response.json().get('ip', 'Unable to fetch IP')
    return render_template("index.html", ip=ip)

@app.route('/health')
def health():
    return 'OK', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)