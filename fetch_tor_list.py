import requests
import logging
import sqlite3

TOR_LIST_URL = "https://secureupdates.checkpoint.com/IP-list/TOR.txt"

logging.basicConfig(level=logging.INFO)


def fetch_tor_list():
    try:
        response = requests.get(TOR_LIST_URL)
        response.raise_for_status()
        logging.info("Fetched Tor exit node list successfully.")
        return response.text.splitlines()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch Tor list: {e}")
        return []


def store_tor_list(ip_list):
    conn = sqlite3.connect('tor_list.db')
    c = conn.cursor()
     ##TODO:// THIS IS PROBABLY NOT THE BEST WAY TO DO THIS
    c.execute('''CREATE TABLE IF NOT EXISTS tor_ips (ip TEXT PRIMARY KEY)''')
    for ip in ip_list:
        c.execute('INSERT OR IGNORE INTO tor_ips (ip) VALUES (?)', (ip, ))
    conn.commit()
    conn.close()
    logging.info("Stored Tor exit node list successfully.")


if __name__ == "__main__":
    ip_list = fetch_tor_list()
    store_tor_list(ip_list)
