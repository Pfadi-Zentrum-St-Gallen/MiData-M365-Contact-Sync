# MiData-M365-Contact-Sync

## General Architecture (Not Final)

```
+----------------+     +---------------------+     +-----------------+
|  MiData API    |     |   Contact Sync      |     |  Microsoft      |
| (Events/People)<-----> Service             <-----> Graph (Contacts |
+----------------+     +-----+-----------+---+     |  & Groups)      |
                             |           |         +-----------------+
                       +-----v-----+ +---v----+
                       | AHV Anchor| | Camp   |
                       |  Database | | DB     |
                       +-----------+ +--------+
```

---

### File Sturcture (Not Final)

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
│   ├── camp_sync.sh           # Camp group creation/deletion logic
│   └── membership.sh          # Add/remove users from groups

-- Not sure design wise
├── db/                        # Track camps & groups (JSON-based "database")
│   └── active_camps.json      # {"camp_id": "123", "m365_group_id": "xyz", "end_date": "2024-0
--

├── logs/
│   └── sync.log               # Logs (rotated by logrotate)
└── docker/
    └── Dockerfile             # Docker build setup
```
