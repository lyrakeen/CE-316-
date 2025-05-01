import os
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

def save_configuration(new_config, file_path):
    """Yeni konfigürasyonu mevcut listeye ekleyerek kaydeder."""
    existing_configs = []

    # Dosya varsa, önce içeriğini oku
    if os.path.exists(file_path):
        try:
            with open(file_path, 'r') as file:
                existing_configs = json.load(file)
                if not isinstance(existing_configs, list):
                    existing_configs = [existing_configs]  # tek kayıt varsa listele
        except json.JSONDecodeError:
            print("[!] Existing file is not valid JSON. Overwriting.")

    # Yeni konfigürasyonu listeye ekle
    existing_configs.append(new_config)

    # Dosyayı tekrar yaz
    try:
        with open(file_path, 'w') as file:
            json.dump(existing_configs, file, indent=4)
        print(f"[✓] Configuration added to {file_path}")
    except Exception as e:
        print(f"[!] Failed to save configuration: {e}")