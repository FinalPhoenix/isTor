from flask import Flask, request, jsonify, render_template
import sqlite3

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('tor_list.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route("/")
def homepage():
    return render_template('homepage.html')

@app.route("/ip/<ip>", methods=["GET"])
def check_ip(ip):
    conn = get_db_connection()
    ip_entry = conn.execute('SELECT * FROM tor_ips WHERE ip = ?', (ip,)).fetchone()
    conn.close()
    if ip_entry:
        return jsonify({"ip": ip, "tor_exit_node": True})
    else:
        return jsonify({"ip": ip, "tor_exit_node": False})

@app.route("/ips", methods=["GET"])
def get_all_ips():
    conn = get_db_connection()
    ips = conn.execute('SELECT * FROM tor_ips').fetchall()
    conn.close()
    return jsonify({"ips": [dict(ip) for ip in ips]})

@app.route("/ip/<ip>", methods=["DELETE"])
def delete_ip(ip):
    conn = get_db_connection()
    conn.execute('DELETE FROM tor_ips WHERE ip = ?', (ip,))
    conn.commit()
    conn.close()
    return jsonify({"message": f"IP {ip} deleted from the list."})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)