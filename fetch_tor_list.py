import requests
import logging
import sqlite3
from requests.exceptions import RequestException
import os
import ipaddress

TOR_LIST_URL = "https://secureupdates.checkpoint.com/IP-list/TOR.txt"

logging.basicConfig(level=logging.INFO)

DB_PATH = os.path.join(os.getcwd(), 'tor_list_data', 'tor_list.db')

def fetch_tor_list():
    try:
        response = requests.get(TOR_LIST_URL)
        response.raise_for_status()
        logging.info("Fetched Tor exit node list successfully.")
        return response.text.splitlines()
    except RequestException as e:
        logging.error(f"Failed to fetch Tor list: {e}")
        return []

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def expand_ip(ip):
    return str(ipaddress.ip_address(ip).exploded)

def sanitize_ip_list(ip_list):
    cleaned_ip_list = [ip.strip('[]') for ip in ip_list]  # Remove brackets
    return [expand_ip(ip) for ip in cleaned_ip_list if is_valid_ip(ip)]

def store_tor_list(ip_list):
    try:
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with sqlite3.connect(DB_PATH, check_same_thread=False) as conn:
            c = conn.cursor()
            c.execute(
                '''CREATE TABLE IF NOT EXISTS tor_ips (ip TEXT PRIMARY KEY)''')
            c.executemany('INSERT OR IGNORE INTO tor_ips (ip) VALUES (?)',
                          [(ip,) for ip in ip_list])
            conn.commit()
        logging.info("Stored Tor exit node list successfully.")
    except sqlite3.Error as e:
        logging.error(f"Failed to store Tor list: {e}")

if __name__ == "__main__":
    ip_list = fetch_tor_list()
    if ip_list:
        sanitized_ip_list = sanitize_ip_list(ip_list)
        store_tor_list(sanitized_ip_list)
    else:
        logging.error("No IPs fetched, nothing to store.")