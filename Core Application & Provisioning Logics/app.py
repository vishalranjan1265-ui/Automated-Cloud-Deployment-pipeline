import os
import sys
import socket
import logging
from flask import Flask, jsonify, Response

logging.basicConfig(
    level=logging.INFO,
    format='{"timestamp":"%(asctime)s", "service":"AppEngine", "level":"%(levelname)s", "message":"%(message)s"}',
    stream=sys.stdout
)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index() -> Response:
    logger.info("Index route accessed successfully.")
    return jsonify({
        "application": "Cloud Automated Deployment Pipeline Target",
        "status": "OPERATIONAL",
        "hostname": socket.gethostname(),
        "environment": os.getenv("APP_ENV", "production")
    })

@app.route("/health", methods=["GET"])
def health_check() -> Response:
    logger.info("Health verification probe requested.")
    return jsonify({
        "status": "UP",
        "container_id": socket.gethostname()
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)