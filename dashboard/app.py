from flask import Flask, render_template
import requests

app = Flask(__name__)
ORION_URL = "http://orion:1026/ngsi-ld/v1"

@app.route('/')
def index():
    data = requests.get(f"{ORION_URL}/entities/urn:ngsi-ld:TrafficSensor:001").json()
    return render_template('index.html', data=data)

@app.route('/update', methods=['POST'])
def update():
    data = request.json
    return "OK"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
