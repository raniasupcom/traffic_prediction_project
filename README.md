🚦 Système de Prédiction de Trafic avec Jumeaux Numériques


📌 Contexte

L’urbanisation rapide engendre une densité croissante du trafic. Pour optimiser la gestion du trafic en temps réel, ce projet propose une solution basée sur des Jumeaux Numériques :

TrafficSensor : Représente les capteurs de trafic en temps réel.

RouteProvider : Fournit des recommandations d’itinéraires basées sur l’état de la circulation.


📘 Explication

orion : Contexte broker FIWARE Orion-LD

mongodb : Stockage des entités NGSI-LD

traffic-sensor : Microservice Flask simulant un capteur

route-provider : Microservice Flask gérant les décisions d’itinéraires dynamiques

🔧 Technologies utilisées :

FIWARE Orion-LD (Broker contextuel)

Docker / Docker Compose

Python (Flask) pour les services backend

🧠 Modèles de Données (NGSI-LD)
1. 📍 TrafficSensor


{
  "id": "urn:ngsi-ld:TrafficSensor:001",
  "type": "TrafficSensor",
  "location": {
    "type": "GeoProperty",
    "value": {
      "type": "Point",
      "coordinates": [2.2945, 48.8584]
    }
  },
  "vehicleCount": {
    "type": "Property",
    "value": 80
  }
}

2. 🚗 RouteProvider


{
  "id": "urn:ngsi-ld:RouteProvider:001",
  "type": "RouteProvider",
  "congestionStatus": {
    "type": "Property",
    "value": {
      "level": "Medium",
      "decision": "Maintain current route",
      "lastUpdated": "2024-07-16T14:30:00Z"
    }
  },
  "trafficSource": {
    "type": "Relationship",
    "object": "urn:ngsi-ld:TrafficSensor:001"
  }
}



⚙️ Installation avec Docker Compose
✅ Prérequis


docker --version        # >= 20.10
docker-compose --version  # >= 2.2




🚀 Lancement de l'application
bash
Copy
Edit
# 1. Clonez le projet
git clone [https://github.com/votre-utilisateur/traffic-dt.git](https://github.com/raniasupcom/traffic_prediction_project.git)
cd traffic-prediction

# 2. Lancez les conteneurs
docker-compose up -d --build

Le contenu docker-compose.yml

services:
  orion:
    image: fiware/orion-ld
    ports:
      - "1026:1026"
    command: -dbhost mongodb

  mongodb:
    image: mongo:4.4
    ports:
      - "27017:27017"

  vehicle_provider:
    build: ./vehicle_provider
    ports:
      - "5001:5000"
    depends_on:
      - orion

  ai_service:
    build: ./ai_service
    ports:
      - "5000:5000"
    depends_on:

Ports exposés :
Orion : 1026

MongoDB : 27017

vehicle_provider : 5001 (interne 5000)

ai_service : 5000


# 3. Ajoutez les entités NGSI-LD

curl -X POST 'http://localhost:1026/ngsi-ld/v1/entities' \
  -H 'Content-Type: application/ld+json' \
  -H 'Link: <https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld>; rel="context"' \
  -d '{
    "id": "urn:ngsi-ld:TrafficSensor:002",
    "type": "TrafficSensor",
    "location": {
      "type": "GeoProperty",
      "value": {
        "type": "Point",
        "coordinates": [2.2845, 48.8584]
      }
    },
    "vehicleCount": {
      "type": "Property",
      "value": 170
    },
    "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
  }'


curl -X POST 'http://localhost:1026/ngsi-ld/v1/entities' \
  -H 'Content-Type: application/ld+json' \
  -H 'Link: <https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld>; rel="context"' \
  -d '{
    "id": "urn:ngsi-ld:RouteProvider:002",
    "type": "RouteProvider",
    "congestionStatus": {
      "type": "Property",
      "value": {
        "level": "Medium",
        "decision": "Maintain current route",
        "lastUpdated": "2024-07-16T14:30:00Z"
      }
    },
    "trafficSource": {
      "type": "Relationship",
      "object": "urn:ngsi-ld:TrafficSensor:003"
    },
    "@context": "https://uri.etsi.org/ngsi-ld/v1/ngsi-ld-core-context.jsonld"
  }'



# Trigger update
curl -X PATCH 'http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:TrafficSensor:001/attrs' \
-H 'Content-Type: application/json' \
-d '{"vehicleCount": {"value": 120}}'

# Verify output
curl 'http://localhost:1026/ngsi-ld/v1/entities/urn:ngsi-ld:RouteProvider:001 | jq '
  # 4. Pour le fonctionnement de dashboard
  flask run --port=8000
  
🗂️ Structure du projet

.
├── docker-compose.yml
├── traffic-sensor/
│   ├── app.py              
│   └── requirements.txt
├── route-provider/
│   ├── app.py              
│   └── Dockerfile
├── dashboard/
│   ├── app.py    
│   └── templates/index.html        


📸 Résultats & Captures d’écran

📍 Architecture globale

![image](https://github.com/user-attachments/assets/8f391781-3194-4d39-84db-519947ac45b6)



📊 Dashboard (Exemples)
![image](https://github.com/user-attachments/assets/06af6fe8-fdbf-4054-91a8-c9bd0935add8)
