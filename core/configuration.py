import json

def load_configuration(file_path):
    """Load configuration data from a JSON file."""
    try:
        with open(file_path, 'r') as file:
            config = json.load(file)
        return config
    except FileNotFoundError:
        print(f"[!] Configuration file not found: {file_path}")
        return None
    except json.JSONDecodeError:
        print(f"[!] Configuration file is not a valid JSON: {file_path}")
        return None

def save_configuration(config_data, file_path):
    """Save configuration data to a JSON file."""
    try:
        with open(file_path, 'w') as file:
            json.dump(config_data, file, indent=4)
        print(f"[✓] Configuration saved to {file_path}")
    except Exception as e:
        print(f"[!] Failed to save configuration: {e}")
