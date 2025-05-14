import requests
import json
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# API-Konfiguration aus Umgebungsvariablen
url = os.getenv("API_BASE_URL")
api_key = os.getenv("API_KEY")

if not url or not api_key:
    print("Fehler: API_BASE_URL oder API_KEY ist nicht in der .env-Datei definiert.")
    exit(1)

params = {
    "include": "layer_group",
    "filter[updated_at][gt]": "2025-01-01T00:00:00.000Z"
}
headers = {
    "accept": "application/vnd.api+json",
    "X-TOKEN": api_key
}

# API-Anfrage
response = requests.get(url, headers=headers, params=params)

# Überprüfen, ob die Anfrage erfolgreich war
if response.status_code == 200:
    # Antwort in eine JSON-Datei schreiben
    with open("output.json", "w") as file:
        json.dump(response.json(), file, indent=4)
    print("Die Antwort wurde erfolgreich in 'output.json' gespeichert.")
else:
    print(f"Fehler: {response.status_code} - {response.text}")