def filter_by_layer_group(data, layer_group_id):
    """Return list of people that belong to the specified layer group."""
    return [
        person
        for person in data.get("data", [])
        if person.get("relationships", {}).get("layer_group", {}).get("data", {}).get("id") == str(layer_group_id)
    ]
