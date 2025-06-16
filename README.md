# Contact Sync Service: MiData (Hitobito) ↔ Microsoft 365

This project synchronises ScoutCH Hitobito members to Microsoft 365 contacts.
It now exposes a small Python package called **`contact_sync`** which contains
utilities for fetching members, filtering them and pushing updates via the
Microsoft Graph API.

## Usage

1. Create a `.env` file based on `.env.example` and provide the required keys.
   The `LAYER_GROUP_ID` determines which Hitobito layer group will be
   synchronised.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Run the consumer:
   ```bash
   python sync_contacts.py
   ```
4. Alternatively use the package directly:
   ```bash
   python -m contact_sync
   ```

## Planned Feature set
- **Contact Sync**: Directional sync of MiData members to M365 contacts.
- **Camp Automation**: Auto-create/delete M365 distribution groups for active camps.
- **Hard Matching**: Uses encrypted **PBS ID** for reliable delta syncs.
- **CLI Management**: Configure schedules, secrets, and manual syncs.
- **Security**: Certificate auth, encrypted secrets, and least-privilege permissions.
