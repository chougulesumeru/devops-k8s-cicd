# A minimal REST API with two endpoints: a health and database connected 
# endpoint. 

import os
import psycopg2
from flask import Flask, jsonify

app = Flask(__name__)

# Read DB credentials from environment variables (injected via K8s Secret)
DB_HOST = os.environ.get("DB_HOST", "postgres-svc")
DB_NAME = os.environ.get("DB_NAME", "appdb")
DB_USER = os.environ.get("DB_USER", "appuser")
DB_PASS = os.environ.get("DB_PASS", "apppassword")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST, dbname=DB_NAME,
        user=DB_USER, password=DB_PASS
    )

@app.route("/health")
def health():
    """Used by Kubernetes liveness probe — just returns OK."""
    return jsonify({"status": "ok"}), 200

@app.route("/ready")
def ready():
    """Used by Kubernetes readiness probe — verifies DB is reachable."""
    try:
        conn = get_db_connection()
        conn.close()
        return jsonify({"status": "ready", "db": "connected"}), 200
    except Exception as e:
        return jsonify({"status": "not ready", "error": str(e)}), 503

@app.route("/")
def index():
    return jsonify({"message": "Flask + PostgreSQL on Kubernetes!"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)