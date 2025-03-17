# MiData-M365-Contact-Sync
```
+----------------+       +---------------------+       +-----------------+
|                |       |   Contact Sync      |       |                 |
|  MiData API    <-------> Service (Bash)      <-------> Microsoft Graph |
|                | HTTPS | Docker Container    | HTTPS | (M365 Contacts) |
+----------------+       +-----+-----------+---+       +-----------------+
                               |           |
                               |           |
                     +---------v-+   +-----v---------+
                     | Config &  |   | Logs &        |
                     | Secrets   |   | Audit Trails  |
                     +-----------+   +---------------+
```
