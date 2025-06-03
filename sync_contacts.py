import json
import requests
import pika
from dotenv import load_dotenv
import os

# .env-Datei laden
load_dotenv()

# Konfiguration aus .env-Datei
RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = os.getenv("QUEUE_NAME", "contact.sync")
GRAPH_API_BASE_URL = os.getenv("GRAPH_API_BASE_URL", "https://graph.microsoft.com/v1.0")
M365_USER_ID = os.getenv("M365_USER_ID", "me")
GRAPH_API_TOKEN = os.getenv("GRAPH_API_TOKEN")

if not GRAPH_API_TOKEN:
    print("Fehler: GRAPH_API_TOKEN ist nicht in der .env-Datei definiert.")
    exit(1)

# Authentifizierung für Microsoft Graph API
def ms_graph_auth():
    return f"Bearer {GRAPH_API_TOKEN}"

# Abrufen bestehender Kontakte aus M365
def get_existing_contacts():
    token = ms_graph_auth()
    url = f"{GRAPH_API_BASE_URL}/users/{M365_USER_ID}/contacts"
    headers = {"Authorization": token}
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return {contact["id"]: contact for contact in response.json().get("value", [])}
    else:
        print(f"Fehler beim Abrufen der Kontakte: {response.status_code} - {response.text}")
        return {}

# Erstellen eines neuen Kontakts in M365
def create_contact(data):
    token = ms_graph_auth()
    url = f"{GRAPH_API_BASE_URL}/users/{M365_USER_ID}/contacts"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 201:
        print(f"Kontakt erstellt: {data.get('displayName')}")
    else:
        print(f"Fehler beim Erstellen des Kontakts: {response.status_code} - {response.text}")

# Aktualisieren eines bestehenden Kontakts in M365
def update_contact(contact_id, data):
    token = ms_graph_auth()
    url = f"{GRAPH_API_BASE_URL}/users/{M365_USER_ID}/contacts/{contact_id}"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, json=data)
    if response.status_code == 200:
        print(f"Kontakt aktualisiert: {data.get('displayName')}")
    else:
        print(f"Fehler beim Aktualisieren des Kontakts: {response.status_code} - {response.text}")

# Löschen eines Kontakts in M365
def delete_contact(contact_id):
    token = ms_graph_auth()
    url = f"{GRAPH_API_BASE_URL}/users/{M365_USER_ID}/contacts/{contact_id}"
    headers = {"Authorization": token}
    response = requests.delete(url, headers=headers)
    if response.status_code == 204:
        print(f"Kontakt gelöscht: {contact_id}")
    else:
        print(f"Fehler beim Löschen des Kontakts: {response.status_code} - {response.text}")

# Verarbeitung von RabbitMQ-Nachrichten
def process_message(ch, method, properties, body):
    event = json.loads(body)
    print(f"Empfangene Nachricht: {event}")

    # Bestehende Kontakte abrufen
    existing_contacts = get_existing_contacts()

    # Event-Typ verarbeiten
    event_type = event.get("event_type")
    contact_id = event.get("contact_id")
    data = event.get("data")

    if event_type == "created":
        if contact_id not in existing_contacts:
            create_contact(data)
        else:
            print(f"Kontakt existiert bereits: {contact_id}")
    elif event_type == "updated":
        if contact_id in existing_contacts:
            update_contact(contact_id, data)
        else:
            print(f"Kontakt nicht gefunden, wird erstellt: {contact_id}")
            create_contact(data)
    elif event_type == "deleted":
        if contact_id in existing_contacts:
            delete_contact(contact_id)
        else:
            print(f"Kontakt nicht gefunden, kann nicht gelöscht werden: {contact_id}")

# RabbitMQ-Verbindung herstellen und Nachrichten konsumieren
def start_rabbitmq_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)

    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message, auto_ack=True)
    print("Warte auf Nachrichten...")
    channel.start_consuming()

# Hauptprogramm
if __name__ == "__main__":
    start_rabbitmq_consumer()