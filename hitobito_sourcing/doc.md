```Text
[Member DB/API]
     ↓
[Python Fetcher: Detect Changes]
     ↓
[Event JSONs: "created", "updated", "deleted"]
     ↓
[Publish to RabbitMQ]
     ↓
[Worker Consumes JSON]
     ↓
[MS Graph API Calls (Create/Update/Delete Contact)]
```