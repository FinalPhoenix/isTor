import requests
import logging
import sqlite3
from requests.exceptions import RequestException

TOR_LIST_URL = "https://secureupdates.checkpoint.com/IP-list/TOR.txt"

logging.basicConfig(level=logging.INFO)

def fetch_tor_list():
    try:
        response = requests.get(TOR_LIST_URL)
        response.raise_for_status()
        logging.info("Fetched Tor exit node list successfully.")
        return response.text.splitlines()
    except RequestException as e:
        logging.error(f"Failed to fetch Tor list: {e}")
        return []

def store_tor_list(ip_list):
    try:
        with sqlite3.connect('tor_list.db') as conn:
            c = conn.cursor()
            c.execute('''CREATE TABLE IF NOT EXISTS tor_ips (ip TEXT PRIMARY KEY)''')
            c.executemany('INSERT OR IGNORE INTO tor_ips (ip) VALUES (?)', [(ip,) for ip in ip_list])
            conn.commit()
        logging.info("Stored Tor exit node list successfully.")
    except sqlite3.Error as e:
        logging.error(f"Failed to store Tor list: {e}")

if __name__ == "__main__":
    ip_list = fetch_tor_list()
    if ip_list:
        store_tor_list(ip_list)
    else:
        logging.error("No IPs fetched, nothing to store.")