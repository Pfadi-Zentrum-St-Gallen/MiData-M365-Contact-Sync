# Contact Sync Service: MiData (Hitobito) ↔ Microsoft 365

A service to sync **ScoutCH hitobito_pbs** members as contacts to Microsoft 365 (M365) and automate camp-based distribution groups. Uses Microsoft Graph API with security-first design.

---

## Features
- **Contact Sync**: Directional sync of MiData members to M365 contacts.
- **Camp Automation**: Auto-create/delete M365 distribution groups for active camps.
- **Hard Matching**: Uses encrypted **PBS ID** for reliable delta syncs.
- **CLI Management**: Configure schedules, secrets, and manual syncs.
- **Security**: Certificate auth, encrypted secrets, and least-privilege permissions.

---

## Architecture
```Text
+----------------+     +---------------------+     +-----------------+
|  MiData API    |     |   Contact Sync      |     |  Microsoft      |
| (Events/People)<-----> Service (Docker)    <-----> Graph (Contacts |
+----------------+     +-----+-----------+---+     |  & Groups)      |
                             |           |         +-----------------+
                    +--------v-----+ +---v----+
                    | PBS ID Anchor| | Camp   |
                    | Database     | | DB     |
                    +--------------+ +--------+
```

---

## File Structure for POC in Bash (Not realy ment for Production xD)
```bash
/opt/contact-sync/
├── bin/
│   ├── contact-sync           # CLI entrypoint
│   └── sync.sh                # Main sync script
├── config/
│   ├── settings.enc           # Encrypted config (Azure/MiData)
│   └── schedule               # Cron schedule
├── lib/
│   ├── auth.sh                # Microsoft Graph auth
│   ├── midata.sh              # MiData API helpers
│   ├── camp_sync.sh           # Camp group logic
│   └── utils.sh               # AHV encryption/delta sync
├── db/
│   ├── active_camps.json      # Track camp-group mappings
│   └── ahv_anchors.db         # AHV-to-ContactID mappings
├── logs/
│   └── sync.log               # Logs
└── docker/
    └── Dockerfile             # Container setup
```

---

## Setup

### 1. Prerequisites
- Entra AD App with `Contacts.ReadWrite` and `Group.ReadWrite.All` permissions.
- MiData (Hitobito) API access (API key).
- `openssl` installed.

### 2. Configure Secrets
```bash
./contact-sync configure \
  --azure-tenant "contoso.onmicrosoft.com" \
  --midata-apikey "encrypted:XXX" \
  --cert-path ./config/cert.pfx
```

### 3. Build & Run Docker (If wanted)
```bash
docker build -t contact-sync -f docker/Dockerfile .
docker run -d \
  -v ./config:/opt/contact-sync/config \
  -v ./logs:/opt/contact-sync/logs \
  --name contact-sync \
  contact-sync
```

---

## Security
- **PBS ID Hashing**: AES-256 encrypted PBS ID anchor stored in M365 contacts.
  ```bash
  PBSID_encrypted=$(echo "$PBSID" | openssl enc -aes-256-cbc -salt -pass pass:$SECRET_KEY | base64)
  ```
- **Entra AD Auth**: Certificate-based authentication (no client secrets).
- **Secrets Management**: Encrypted `settings.enc` using `openssl`.

---

## CLI Commands
```bash
# Manual sync (dry-run)
./contact-sync sync-now --dry-run

# Configure camp sync schedule
./contact-sync set-schedule "0 3 * * *"

# List active camps/groups
./contact-sync list-camps

# Rotate encryption keys
./contact-sync rotate-key --new-key $(openssl rand -hex 32)
```

---

## Camp Sync Workflow
1. **Detect Active Camps**: Poll MiData (Hitobito) for `GET /events.json?type=camp&state=open`.
2. **Create M365 Group**: Auto-provision a security group for new camps.
3. **Sync Participants**: Add members to the group via AHV-based matching.
4. **Cleanup**: Delete groups when camps close (based on `end_date`).

---

## Delta Sync with PBS ID Anchors
- **Hard Matching**: Contacts are matched using encrypted PBS ID stored in M365 `notes` field.
- **Efficiency**: Only new/changed contacts are synced.
  ```bash
  # Transform AHV to encrypted anchor
  jq -c --arg PBSID "$PBSID_encrypted" '.notes = "SourceAnchor:\($PBSID)"'
  ```
