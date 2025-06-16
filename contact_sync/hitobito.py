import json
import requests
from .config import API_BASE_URL, API_KEY


def fetch_members(params=None):
    """Fetch member data from Hitobito API and return JSON."""
    if API_KEY is None:
        raise RuntimeError("API_KEY is not configured")
    headers = {
        "accept": "application/vnd.api+json",
        "X-TOKEN": API_KEY,
    }
    response = requests.get(API_BASE_URL, headers=headers, params=params)
    response.raise_for_status()
    return response.json()


def save_json(data, path="output.json"):
    with open(path, "w") as f:
        json.dump(data, f, indent=4)
