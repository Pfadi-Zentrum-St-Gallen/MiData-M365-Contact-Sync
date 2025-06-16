import os
from dotenv import load_dotenv

load_dotenv()

API_BASE_URL = os.getenv("API_BASE_URL", "https://db.scout.ch/api/people")
API_KEY = os.getenv("API_KEY")

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")
QUEUE_NAME = os.getenv("QUEUE_NAME", "contact.sync")
GRAPH_API_BASE_URL = os.getenv("GRAPH_API_BASE_URL", "https://graph.microsoft.com/v1.0")
M365_USER_ID = os.getenv("M365_USER_ID", "me")
GRAPH_API_TOKEN = os.getenv("GRAPH_API_TOKEN")

# Hitobito layer group used for filtering members
LAYER_GROUP_ID = os.getenv("LAYER_GROUP_ID", "6855")
