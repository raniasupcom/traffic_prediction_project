# 🚦 Real-Time Traffic Prediction with FIWARE



## 📦 Quick Deployment
```bash
# 1. Clone repository
git clone https://github.com/raniasupcom/traffic-prediction.git
cd traffic-prediction

# 2. Start services
docker-compose up -d --build

# 3. Initialize (wait 60s)
sleep 60

# 4. Set up subscriptions
curl -X POST 'http://localhost:1026/ngsi-ld/v1/subscriptions' -H 'Content-Type: application/json' -d '{
  "description": "Traffic to AI",
  "type": "Subscription",
  "entities": [{"type": "TrafficSensor"}],
  "watchedAttributes": ["vehicleCount"],
  "notification": {
    "endpoint": {
      "uri": "http://ai_service:5000/predict",
      "accept": "application/json"
    }
  }
}'
