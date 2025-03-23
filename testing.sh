#!/bin/bash

####################################################################################
# Script Name: testing.sh
# Description: Dieses Skript lädt Konfigurationswerte aus einer .env-Datei und
#              führt eine API-Anfrage durch, um alle Personen aus einer bestimmten
#              Pfadigruppe abzurufen.
# Author:      Frederik Sinniger
# Date:        23. März 2025
# Version:     1.0
# Usage:       ./testing.sh
# Notes:       Stellen Sie sicher, dass eine .env-Datei im gleichen Verzeichnis
#              wie dieses Skript vorhanden ist und die erforderlichen Variablen
#              definiert sind.
# Dependencies: curl
####################################################################################

# .env-Datei laden
if [ -f .env ]; then
  export $(cat .env | xargs)
fi

