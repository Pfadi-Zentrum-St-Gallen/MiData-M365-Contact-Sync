import json
import pika

from .config import RABBITMQ_HOST, QUEUE_NAME
from .graph_api import get_existing_contacts, create_contact, update_contact, delete_contact


def process_message(ch, method, properties, body):
    event = json.loads(body)
    event_type = event.get("event_type")
    contact_id = event.get("contact_id")
    data = event.get("data")

    contacts = get_existing_contacts()

    if event_type == "created":
        if contact_id not in contacts:
            create_contact(data)
    elif event_type == "updated":
        if contact_id in contacts:
            update_contact(contact_id, data)
        else:
            create_contact(data)
    elif event_type == "deleted":
        if contact_id in contacts:
            delete_contact(contact_id)


def start_consumer():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME)
    channel.basic_consume(queue=QUEUE_NAME, on_message_callback=process_message, auto_ack=True)
    print("Waiting for messages...")
    channel.start_consuming()
