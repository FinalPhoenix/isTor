from flask import Flask, request, jsonify
from flasgger import Swagger
import sqlite3
import ipaddress
import threading
import time
import os
from fetch_tor_list import fetch_tor_list, store_tor_list, sanitize_ip_list, expand_ip

app = Flask(__name__)

swagger_config = {
    "headers": [],
    "info": {
        "title": "isTor API",
        "description": "An API to check if an IP address is a Tor exit node, retrieve all Tor exit nodes, and delete specific IP addresses from the list.",
        "version": "1.0.0"
    },
    "specs": [{
        "endpoint": 'apispec_1',
        "route": '/apispec_1.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path": "/flasgger_static",
    "swagger_ui": True,
    "specs_route": "/"
}
swagger = Swagger(app, config=swagger_config)

DB_PATH = os.path.join(os.getcwd(), 'tor_list_data', 'tor_list.db')

def get_db_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/ip/<ip>", methods=["GET"])
def check_ip(ip):
    """
    Check if an IP is a Tor exit node
    ---
    parameters:
      - name: ip
        in: path
        type: string
        required: true
        description: The IP address to check
    responses:
      200:
        description: The result of the check
        schema:
          type: object
          properties:
            ip:
              type: string
            tor_exit_node:
              type: boolean
    """
    try:
        ip_address = expand_ip(ip)
    except ValueError:
        return jsonify({"error": "Invalid IP address format"}), 400

    conn = get_db_connection()
    try:
        ip_entry = conn.execute('SELECT * FROM tor_ips WHERE ip = ?',
                                (ip_address, )).fetchone()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    if ip_entry:
        return jsonify({"ip": ip_address, "tor_exit_node": True})
    else:
        return jsonify({"ip": ip_address, "tor_exit_node": False})

@app.route("/ips", methods=["GET"])
def get_all_ips():
    """
    Get all Tor exit node IPs
    ---
    responses:
      200:
        description: A list of Tor exit node IPs
        schema:
          type: object
          properties:
            ips:
              type: array
              items:
                type: object
                properties:
                  ip:
                    type: string
    """
    conn = get_db_connection()
    try:
        ips = conn.execute('SELECT * FROM tor_ips').fetchall()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    return jsonify({"ips": [dict(ip) for ip in ips]})

@app.route("/ip/<ip>", methods=["DELETE"])
def delete_ip(ip):
    """
    Delete an IP from the list
    ---
    parameters:
      - name: ip
        in: path
        type: string
        required: true
        description: The IP address to delete
    responses:
      200:
        description: Deletion result
        schema:
          type: object
          properties:
            message:
              type: string
    """
    try:
        ip_address = expand_ip(ip)
    except ValueError:
        return jsonify({"error": "Invalid IP address format"}), 400

    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM tor_ips WHERE ip = ?', (ip_address, ))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    return jsonify({"message": f"IP {ip_address} deleted from the list."})

def run_scheduler():
    REFRESH_INTERVAL = 24 * 60 * 60  # Refresh every 24 hours

    while True:
        ip_list = fetch_tor_list()
        if ip_list:
            sanitized_ip_list = sanitize_ip_list(ip_list)
            store_tor_list(sanitized_ip_list)
        time.sleep(REFRESH_INTERVAL)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    app.run(host='0.0.0.0', port=5000)
