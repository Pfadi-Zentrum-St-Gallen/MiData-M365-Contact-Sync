# MiData-M365-Contact-Sync

Diese Repository enthält ein Tool zum Synchronisieren von Kontakten zwischen MiData und Microsoft 365.

## Dependency Management

Dieses Projekt verwendet automatisiertes Dependency Management für die MiData Powershell-Bibliothek:

- Die neueste Version von [Hitobito-MiData-Powershell](https://github.com/Pfadi-Zentrum-St-Gallen/Hitobito-MiData-Powershell.git) wird automatisch wöchentlich über einen GitHub Actions-Workflow aktualisiert.
- Der Workflow `update-midata-powershell.yml` lädt die neueste Version herunter und speichert sie im `lib/midata-powershell`-Verzeichnis.
- Der Workflow kann auch manuell über die GitHub-Oberfläche unter "Actions" ausgelöst werden.

### GitHub Workflow Konfiguration

Um den automatischen Update-Workflow korrekt auszuführen, müssen Sie ein persönliches Zugriffstoken (PAT) einrichten:

1. Erstellen Sie ein neues PAT in Ihren GitHub-Einstellungen:
   - Gehen Sie zu GitHub → Settings → Developer settings → Personal access tokens → Tokens (classic)
   - Klicken Sie auf "Generate new token (classic)"
   - Geben Sie einen Namen ein (z.B. "MiData-M365-Contact-Sync CI")
   - Wählen Sie mindestens die "repo"-Berechtigung
   - Klicken Sie auf "Generate token" und kopieren Sie das generierte Token

2. Fügen Sie das Token als Repository-Secret hinzu:
   - Gehen Sie zum Repository → Settings → Secrets and variables → Actions
   - Klicken Sie auf "New repository secret"
   - Name: `GH_PAT`
   - Value: [Ihr kopiertes Token]
   - Klicken Sie auf "Add secret"

Der Workflow verwendet dieses Token, um Änderungen zurück in das Repository zu pushen.

## Manuelles Update der MiData Powershell-Bibliothek

Falls Sie die Bibliothek manuell aktualisieren möchten, können Sie den folgenden Befehl verwenden:

```powershell
# Temporäres Verzeichnis erstellen
New-Item -ItemType Directory -Path .\temp_midata -Force

# Repository klonen
git clone https://github.com/Pfadi-Zentrum-St-Gallen/Hitobito-MiData-Powershell.git .\temp_midata

# Zielverzeichnis erstellen falls nicht vorhanden
New-Item -ItemType Directory -Path .\lib\midata-powershell -Force

# Dateien kopieren
Copy-Item -Path .\temp_midata\* -Destination .\lib\midata-powershell -Recurse -Force

# Temporäres Verzeichnis entfernen
Remove-Item -Path .\temp_midata -Recurse -Force
```

## Verzeichnisstruktur

```
MiData-M365-Contact-Sync/
├── .github/
│   └── workflows/
│       └── update-midata-powershell.yml
├── lib/
│   └── midata-powershell/  # Enthält die aktuellste Version von Hitobito-MiData-Powershell
├── LICENSE
└── README.md
```