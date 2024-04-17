import json

def parse_json(data):
    try:
        return json.loads(data)
    except json.JSONDecodeError as e:
        print(f"Failed to decode JSON: {e}")
        return None