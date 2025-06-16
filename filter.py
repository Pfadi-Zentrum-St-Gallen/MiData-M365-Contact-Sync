import json
from contact_sync.filtering import filter_by_layer_group


def main(path="output.json", layer_group_id="6855"):
    with open(path, "r") as file:
        data = json.load(file)

    filtered = filter_by_layer_group(data, layer_group_id)

    print(f"Gefundene Personen in Layer Group {layer_group_id}:")
    for person in filtered:
        attrs = person.get("attributes", {})
        print(f"- {attrs.get('first_name')} {attrs.get('last_name')} ({attrs.get('email')})")


if __name__ == "__main__":
    main()
