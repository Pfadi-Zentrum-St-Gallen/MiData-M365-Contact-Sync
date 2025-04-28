# Contact Sync Service: MiData (Hitobito) ↔ Microsoft 365

A service to sync **ScoutCH hitobito_pbs** members as contacts to Microsoft 365 (M365) and automate camp-based distribution groups. Uses Microsoft Graph API with security-first design.

---

## Planned Feature set
- **Contact Sync**: Directional sync of MiData members to M365 contacts.
- **Camp Automation**: Auto-create/delete M365 distribution groups for active camps.
- **Hard Matching**: Uses encrypted **PBS ID** for reliable delta syncs.
- **CLI Management**: Configure schedules, secrets, and manual syncs.
- **Security**: Certificate auth, encrypted secrets, and least-privilege permissions.

---

## Architecture
```Text
+-------------------+            +-------------------+            +-------------------+
|                   |            |                   |            |                   |
|   Hitobito API    +----------->+   Messaging Queue +----------->+  M365 Sync Worker |
|                   |            |                   |            |                   |
| (Polling/Change   |            | (e.g., RabbitMQ,  |            | (Consumes from    |
|  Detection)       |            | Kafka, or Azure)  |            | Queue & Pushes to |
|                   |            |                   |            | M365 Graph API)   |
+-------------------+            +-------------------+            +-------------------+
        |                             |                                     |
        |                             |                                     |
        v                             v                                     v
+-------------------+   +---------------------------+   +---------------------------+
|   Normalization   |   |   Reliable Delivery w/    |   |  Error Handling & Retry   |
|   & Deduplication |   |   Ordering & Retries      |   |  (Dead-Letter Queue)      |
+-------------------+   +---------------------------+   +---------------------------+
```
