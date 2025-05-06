from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes
ORION_URL = "http://orion:1026/ngsi-ld/v1"

@app.route('/')
def index():
    try:
        data = requests.get(f"{ORION_URL}/entities/urn:ngsi-ld:TrafficSensor:001").json()
        return render_template('index.html', data=data)
    except Exception as e:
        return f"Error fetching data: {str(e)}", 500

@app.route('/update', methods=['POST'])
def update():
    try:
        data = request.json
        # Add your update logic here
        return jsonify({"status": "OK"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
