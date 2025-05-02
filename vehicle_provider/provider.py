import random
import requests
from flask import Flask

app = Flask(__name__)
ORION_URL = "http://orion:1026/ngsi-ld/v1"

# Initialize entity
requests.post(f"{ORION_URL}/entities", json={
    "id": "urn:ngsi-ld:TrafficSensor:001",
    "type": "TrafficSensor",
    "vehicleCount": {"type": "Property", "value": 0},
    "congestionLevel": {"type": "Property", "value": "Unknown"}
})

@app.route('/update')
def update_count():
    new_count = random.randint(0, 200)
    response = requests.patch(
        f"{ORION_URL}/entities/urn:ngsi-ld:TrafficSensor:001/attrs",
        json={"vehicleCount": {"value": new_count, "type": "Property"}}
    )
    return f"Updated count to {new_count}"

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
