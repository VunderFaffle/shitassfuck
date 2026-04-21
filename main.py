from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)  # allow CORS for all domains

alerts_db = []


# creating alert
@app.route("/api/alerts", methods=["POST"])
def create_alert():
    data = request.get_json()

    # simple validation
    if not data:
        return jsonify({"error": "No data"}), 400

    title = data.get("title")
    description = data.get("description", "")
    address = data.get("address")
    level = data.get("level", "info")

    if not title or not address:
        return jsonify({"error": "Missing fields"}), 400

    alert = {
        "id": len(alerts_db) + 1,
        "title": title,
        "description": description,
        "address": address,
        "level": level,
        "timestamp": datetime.utcnow().isoformat()
    }

    alerts_db.insert(0, alert)

    return jsonify({"status": "ok", "alert": alert})

@app.route("/api/alerts/<int:alert_id>", methods=["DELETE"])
def delete_alert(alert_id):
    auth = request.headers.get("Authorization")

    if auth != "Bearer secret-token":
        return jsonify({"error": "Unauthorized"}), 401

    global alerts_db

    alerts_db = [a for a in alerts_db if a["id"] != alert_id]

    return jsonify({"status": "deleted"})

# get alerts
@app.route("/api/alerts", methods=["GET"])
def get_alerts():
    return jsonify(alerts_db)


# login
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json()

    if data.get("login") == "admin" and data.get("password") == "admin":
        return jsonify({"token": "secret-token"})

    return jsonify({"error": "Invalid credentials"}), 401


# healthcheck
@app.route("/")
def home():
    return "Backend is running"


if __name__ == "__main__":
    app.run(debug=True)