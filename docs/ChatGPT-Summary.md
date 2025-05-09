### ✅ **System Components Overview**

| Component         | Role                                                     |
| ----------------- | -------------------------------------------------------- |
| Member Database   | Source of truth for contact data                         |
| Event Generator   | Detects changes (create/update/delete) in member data    |
| RabbitMQ          | Queues contact change events                             |
| Worker (Consumer) | Consumes events and applies them via Microsoft Graph API |
| MS Graph API      | Target system (M365 Contacts)                            |

---

### 🛠️ **Architecture Flow**

1. **Detect Changes in Member DB**

   * Poll or subscribe to DB change events (e.g., via triggers, logs, or timestamps).
   * Generate events: `ContactCreated`, `ContactUpdated`, `ContactDeleted`.

2. **Publish to RabbitMQ**

   * Serialize each event to JSON and push it to a RabbitMQ queue, e.g., `contact.sync`.

3. **Consume Events**

   * Worker service listens on the queue.
   * Deserializes the message and calls the Microsoft Graph API accordingly.

4. **Graph API Actions**

   * Use OAuth2 + delegated or application permissions.
   * Use endpoints like:

     * `POST /users/{userId}/contacts`
     * `PATCH /users/{userId}/contacts/{contactId}`
     * `DELETE /users/{userId}/contacts/{contactId}`

---

### 🧩 **Detailed Example (Python)**

#### 1. **Event Types**

```python
from dataclasses import dataclass
import json

@dataclass
class ContactEvent:
    event_type: str  # "created", "updated", "deleted"
    contact_id: str
    data: dict  # Full contact data
```

---

#### 2. **Publishing Events to RabbitMQ**

```python
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters("localhost"))
channel = connection.channel()
channel.queue_declare(queue="contact.sync")

def publish_event(event: ContactEvent):
    body = json.dumps(event.__dict__)
    channel.basic_publish(exchange="", routing_key="contact.sync", body=body)
```

---

#### 3. **Consuming & Syncing with M365**

```python
import requests

def ms_graph_auth():
    # Implement client credentials or delegated token retrieval here
    return "Bearer ey..."

def create_contact(data, user_id="me"):
    token = ms_graph_auth()
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/contacts"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    requests.post(url, headers=headers, json=data)

def update_contact(contact_id, data, user_id="me"):
    token = ms_graph_auth()
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/contacts/{contact_id}"
    headers = {"Authorization": token, "Content-Type": "application/json"}
    requests.patch(url, headers=headers, json=data)

def delete_contact(contact_id, user_id="me"):
    token = ms_graph_auth()
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/contacts/{contact_id}"
    headers = {"Authorization": token}
    requests.delete(url, headers=headers)
```

---

#### 4. **RabbitMQ Worker**

```python
def callback(ch, method, properties, body):
    event = json.loads(body)
    print(f"Received event: {event}")
    if event["event_type"] == "created":
        create_contact(event["data"])
    elif event["event_type"] == "updated":
        update_contact(event["contact_id"], event["data"])
    elif event["event_type"] == "deleted":
        delete_contact(event["contact_id"])

channel.basic_consume(queue="contact.sync", on_message_callback=callback, auto_ack=True)
channel.start_consuming()
```

---

### 🛡️ **Tips for Robustness**

* Use idempotent logic (e.g., contact IDs from the source system).
* Implement retry/dead-letter logic on the consumer.
* Encrypt tokens, validate contact schema before pushing.
* Add logging and monitoring.
