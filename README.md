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

---

```
/opt/contact-sync/
├── bin/
│   ├── contact-sync           # CLI entrypoint (symlinked to /usr/local/bin)
│   └── sync.sh                # Main sync script (called by cron/service)
├── config/
│   ├── settings.enc           # Encrypted config (Azure/MiData credentials)
│   └── schedule               # Cron schedule file
├── lib/
│   ├── auth.sh                # Handles Microsoft Graph authentication
│   ├── midata.sh              # MiData API helpers
│   └── utils.sh               # Logging/error handling
├── logs/
│   └── sync.log               # Logs (rotated by logrotate)
└── docker/
    └── Dockerfile             # Docker build setup
```
