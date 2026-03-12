import requests
import numpy as np
from datetime import datetime

# === CONFIGURATION ===
CHANNEL_ID = "2900946"
READ_API_KEY = "FL16TI72OJFPQ71M"  # "" si canal public
INTERVAL = 30  # Délai entre chaque collecte (en secondes)
BATCH_SIZE = 30  # Taille du tableau (30 lignes)


def get_latest_entry():
    url = f"https://api.thingspeak.com/channels/{CHANNEL_ID}/feeds.json"
    params = {"api_key": READ_API_KEY, "results": 1}

    try:
        response = requests.get(url, params=params)
        data = response.json()

        if "feeds" in data and data["feeds"]:
            feed = data["feeds"][0]
            latest_data=np.array([float(feed["field1"]) if feed["field1"] else None, float(feed["field1"]) if feed["field1"] else None, float(feed["field2"]) if feed["field2"] else None,])
            return latest_data

    except Exception as e:
        print("Erreur lors de la récupération :", e)
        return None

