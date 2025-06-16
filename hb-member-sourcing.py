from contact_sync.hitobito import fetch_members, save_json


def main():
    data = fetch_members(params={"include": "layer_group"})
    save_json(data)


if __name__ == "__main__":
    main()
