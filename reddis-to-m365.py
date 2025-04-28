import redis
import json
import time
import requests
from msal import ConfidentialClientApplication

# Configuration
REDIS_HOST = "localhost"
REDIS_PORT = 6379
REDIS_DB = 0
M365_TENANT_ID = "your-tenant-id"
M365_CLIENT_ID = "your-client-id"
M365_CLIENT_SECRET = "your-client-secret"
M365_GRAPH_ENDPOINT = "https://graph.microsoft.com/v1.0/me/contacts"

# Initialize Redis
redis_client = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB, decode_responses=True)

# MSAL Authentication
def get_access_token():
    app = ConfidentialClientApplication(
        client_id=M365_CLIENT_ID,
        client_credential=M365_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{M365_TENANT_ID}"
    )
    token_response = app.acquire_token_for_client(scopes=["https://graph.microsoft.com/.default"])
    if "access_token" in token_response:
        return token_response["access_token"]
    else:
        raise Exception(f"Failed to acquire token: {token_response}")

# Sync contact to Microsoft 365
def sync_contact_to_m365(contact, access_token):
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(M365_GRAPH_ENDPOINT, headers=headers, json=contact)
    if response.status_code == 201:  # Created
        print(f"Successfully synced contact: {contact.get('displayName')}")
        return True
    else:
        print(f"Failed to sync contact: {contact.get('displayName')}. Error: {response.text}")
        return False

# Main sync logic
def sync_contacts():
    access_token = get_access_token()
    while True:
        # Fetch a contact ID from the Redis queue
        contact_id = redis_client.rpop("contacts_to_sync")
        if not contact_id:
            print("No more contacts to sync. Exiting...")
            break

        # Fetch the contact data from Redis
        contact_data = redis_client.get(f"contact:{contact_id}")
        if not contact_data:
            print(f"Contact data not found for ID: {contact_id}. Skipping...")
            continue

        # Parse contact data
        contact = json.loads(contact_data)

        # Sync contact to M365
        success = sync_contact_to_m365(contact, access_token)

        # Retry or delete the contact from Redis
        if success:
            # Remove contact from cache
            redis_client.delete(f"contact:{contact_id}")
        else:
            # Push back to the queue for retry
            retries = redis_client.get(f"contact:{contact_id}:retries") or 0
            retries = int(retries) + 1
            if retries <= 3:  # Retry up to 3 times
                redis_client.set(f"contact:{contact_id}:retries", retries)
                redis_client.lpush("contacts_to_sync", contact_id)
                print(f"Retrying contact ID {contact_id} (Attempt {retries}/3)...")
            else:
                print(f"Failed to sync contact ID {contact_id} after 3 attempts. Skipping...")

        # Optional delay to avoid rate-limiting
        time.sleep(0.5)

if __name__ == "__main__":
    sync_contacts()
