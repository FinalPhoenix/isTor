# app.py
from flask import Flask, request, jsonify
from flasgger import Swagger
import sqlite3
import ipaddress

app = Flask(__name__)

# Configure flasgger to use the root path as the documentation route

swagger_config = {
    "headers": [],
    "info": {
        "title": "isTor API",
        "description":
        "An API to check if an IP address is a Tor exit node, retrieve all Tor exit nodes, and delete specific IP addresses from the list.",
        "version": "1.0.0"
    },
    "specs": [{
        "endpoint": 'apispec_1',
        "route": '/apispec_1.json',
        "rule_filter": lambda rule: True,
        "model_filter": lambda tag: True,
    }],
    "static_url_path":
    "/flasgger_static",
    "swagger_ui":
    True,
    "specs_route":
    "/"
}
swagger = Swagger(app, config=swagger_config)


def get_db_connection():
    conn = sqlite3.connect('tor_list.db')
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
        # Validate the IP address format
        ip_address = ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({"error": "Invalid IP address format"}), 400

    conn = get_db_connection()
    try:
        ip_entry = conn.execute('SELECT * FROM tor_ips WHERE ip = ?',
                                (str(ip_address), )).fetchone()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    if ip_entry:
        return jsonify({"ip": str(ip_address), "tor_exit_node": True})
    else:
        return jsonify({"ip": str(ip_address), "tor_exit_node": False})


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
        # Validate the IP address format
        ip_address = ipaddress.ip_address(ip)
    except ValueError:
        return jsonify({"error": "Invalid IP address format"}), 400

    conn = get_db_connection()
    try:
        conn.execute('DELETE FROM tor_ips WHERE ip = ?', (str(ip_address), ))
        conn.commit()
    except sqlite3.Error as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()

    return jsonify({"message": f"IP {ip_address} deleted from the list."})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)