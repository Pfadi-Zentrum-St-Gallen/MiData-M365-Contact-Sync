# Contact Sync Service: MiData (Hitobito) ↔ Microsoft 365

A service to sync **ScoutCH hitobito_pbs** members as contacts to Microsoft 365 (M365) and automate camp-based distribution groups. Uses Microsoft Graph API with security-first design.

> **ℹ️ Info:**
> Active Development happens in Alpha-1 branch, if you want to see current development State!

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
+-------------------+        +-------------------+        +-------------------+        +-------------------+
|                   |        |                   |        |                   |        |                   |
|   Hitobito DB     | -----> |     Producer      | -----> |     RabbitMQ      | -----> |    Consumer        |
|                   |        | (Delta Detection) |        |                   |        | (MS Graph API)     |
+-------------------+        +-------------------+        +-------------------+        +-------------------+
         |                           |                                  |                          |
         |                           |                                  |                          |
         v                           v                                  v                          v
+-------------------+   +-------------------+            +-------------------+        +-------------------+
|   last_changed    |   |   Compare         |            |   Durable Queue   |        |   Create/Update   |
|                   |   |   vs              |            |                   |        |   Contacts        |
+-------------------+   +-------------------+            +-------------------+        +-------------------+
                                                 Dead-letter Queue (DLQ) for errors
```
