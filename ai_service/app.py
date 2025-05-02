from flask import Flask, request, jsonify
import numpy as np
from tensorflow.keras.models import load_model
import requests

app = Flask(__name__)
model = load_model('model/traffic_model.h5')

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    count = data['vehicleCount']['value']
    prediction = model.predict(np.array([[count]]))
    levels = ["Low", "Medium", "High"]
    result = levels[np.argmax(prediction)]
    
    requests.patch(
        "http://orion:1026/ngsi-ld/v1/entities/urn:ngsi-ld:TrafficSensor:001/attrs",
        json={"congestionLevel": {"value": result, "type": "Property"}}
    )
    return jsonify({"congestion": result})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
