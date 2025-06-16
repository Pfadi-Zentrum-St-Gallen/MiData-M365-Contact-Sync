from .hitobito import fetch_members, save_json
from .filtering import filter_by_layer_group
from .consumer import start_consumer


def main():
    # Example usage: fetch members and start consumer
    members = fetch_members()
    filtered = filter_by_layer_group(members, layer_group_id="6855")
    save_json({"data": filtered})

    start_consumer()


if __name__ == "__main__":
    main()
