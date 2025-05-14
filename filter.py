import json

# JSON-Datei laden
with open("output.json", "r") as file:
    data = json.load(file)

# Filterkriterium: Layer Group ID
target_layer_group_id = "6855"

# Personen filtern, die zur gewünschten Layer Group gehören
filtered_people = [
    person for person in data.get("data", [])
    if person.get("relationships", {}).get("layer_group", {}).get("data", {}).get("id") == target_layer_group_id
]

# Gefilterte Ergebnisse ausgeben
print(f"Gefundene Personen in Layer Group {target_layer_group_id}:")
for person in filtered_people:
    attributes = person.get("attributes", {})
    print(f"- {attributes.get('first_name')} {attributes.get('last_name')} ({attributes.get('email')})")