from flask import Flask, jsonify, request, render_template
import requests
import time
from datetime import datetime

app = Flask(__name__, template_folder='templates')
ORION_URL = "http://localhost:1026/ngsi-ld/v1"
last_update = time.time()

@app.after_request
def add_no_cache_headers(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Pragma"] = "no-cache"
    response.headers["Expires"] = "0"
    return response

@app.route('/')
def dashboard():
    return render_template('index.html')

@app.route('/api/traffic-data')
def get_traffic_data():
    try:
        sensor_id = request.args.get('sensor_id', 'urn:ngsi-ld:TrafficSensor:001')
        route_id = request.args.get('route_id', 'urn:ngsi-ld:RouteProvider:001')

        # Get sensor data
        sensor_res = requests.get(f"{ORION_URL}/entities/{sensor_id}")
        sensor_res.raise_for_status()
        sensor_data = sensor_res.json()

        # Get route data
        route_res = requests.get(f"{ORION_URL}/entities/{route_id}")
        route_res.raise_for_status()
        route_data = route_res.json()

        return jsonify({
            "sensor": {
                "vehicleCount": sensor_data.get("vehicleCount", {}).get("value", 0),
                "location": sensor_data.get("location", {}).get("value", {}).get("coordinates", [0, 0])
            },
            "route": {
                "level": route_data.get("congestionStatus", {}).get("value", {}).get("level", "Unknown"),
                "decision": route_data.get("congestionStatus", {}).get("value", {}).get("decision", "Unknown"),
                "lastUpdated": datetime.now().isoformat()
            }
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Orion request failed: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"Unexpected error: {str(e)}"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
