import requests
import logging

TOR_LIST_URL = "https://secureupdates.checkpoint.com/IP-list/TOR.txt"

logging.basicConfig(level=logging.INFO)

def fetch_tor_list():
    try:
        response = requests.get(TOR_LIST_URL)
        response.raise_for_status()
        logging.info("Fetched Tor exit node list successfully.")
        print(response.text)
        return response.text.splitlines()
    except requests.RequestException as e:
        logging.error(f"Failed to fetch Tor list: {e}")
        return []