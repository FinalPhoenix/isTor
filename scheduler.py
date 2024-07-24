import time
from fetch_tor_list import fetch_tor_list, store_tor_list

REFRESH_INTERVAL = 24 * 60 * 60  # Refresh every 24 hours

while True:
    ip_list = fetch_tor_list()
    store_tor_list(ip_list)
    time.sleep(REFRESH_INTERVAL)