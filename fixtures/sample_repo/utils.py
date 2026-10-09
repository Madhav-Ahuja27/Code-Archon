import json


def load_config(path):
    with open(path) as f:
        return json.load(f)


def save_config(path, data):
    with open(path, "w") as f:
        json.dump(data, f, indent=2)
