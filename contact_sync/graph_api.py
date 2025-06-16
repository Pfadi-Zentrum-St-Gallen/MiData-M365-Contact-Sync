import requests
from .config import GRAPH_API_BASE_URL, M365_USER_ID, GRAPH_API_TOKEN


def _auth_header():
    if GRAPH_API_TOKEN is None:
        raise RuntimeError("GRAPH_API_TOKEN is not configured")
    return {"Authorization": f"Bearer {GRAPH_API_TOKEN}"}


def get_existing_contacts():
    url = f"{GRAPH_API_BASE_URL}/users/{M365_USER_ID}/contacts"
    response = requests.get(url, headers=_auth_header())
    response.raise_for_status()
    return {c["id"]: c for c in response.json().get("value", [])}


def create_contact(data):
    url = f"{GRAPH_API_BASE_URL}/users/{M365_USER_ID}/contacts"
    headers = {**_auth_header(), "Content-Type": "application/json"}
    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def update_contact(contact_id, data):
    url = f"{GRAPH_API_BASE_URL}/users/{M365_USER_ID}/contacts/{contact_id}"
    headers = {**_auth_header(), "Content-Type": "application/json"}
    response = requests.patch(url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


def delete_contact(contact_id):
    url = f"{GRAPH_API_BASE_URL}/users/{M365_USER_ID}/contacts/{contact_id}"
    response = requests.delete(url, headers=_auth_header())
    if response.status_code not in (204, 200):
        response.raise_for_status()
