import json
import os

POPULAR_LANGUAGES = {
    "C": {
        "compile_command": "gcc {main_file} -o {main_dir}/a.out",
        "run_command": "{main_dir}/a.out"
    },
    "C++": {
        "compile_command": "g++ {main_file} -o {main_dir}/a.out",
        "run_command": "{main_dir}/a.out"
    },
    "Java": {
        "compile_command": "javac -d {main_dir} {main_file}",
        "run_command": "java -cp {main_dir} Main"
    },
    "Python": {
        "compile_command": "python -m py_compile {main_file}",
        "run_command": "python {main_file}"
    },
    "Go": {
        "compile_command": "go build -o {main_dir}/app {main_file}",
        "run_command": "{main_dir}/app"
    },
    "Ruby": {
        "compile_command": "ruby -c {main_file}",
        "run_command": "ruby {main_file}"
    },
    "Node.js": {
        "compile_command": "node --check {main_file}",
        "run_command": "node {main_file}"
    },
    "Rust": {
        "compile_command": "rustc {main_file} -o {main_dir}/main",
        "run_command": "{main_dir}/main"
    },
    "Kotlin": {
        "compile_command": "kotlinc {main_file} -include-runtime -d {main_dir}/main.jar",
        "run_command": "java -jar {main_dir}/main.jar"
    }
}


def load_configuration(file_path):
    if not os.path.isabs(file_path) and "configs" not in file_path:
        file_path = os.path.join("configs", file_path)

    if not os.path.exists(file_path):
        print(f"[!] Configuration file not found: {file_path}")
        return None

    try:
        with open(file_path, 'r') as file:
            config = json.load(file)

        # config_name yoksa dosya adından türet
        if "config_name" not in config:
            config["config_name"] = os.path.splitext(os.path.basename(file_path))[0]

        return config
    except json.JSONDecodeError:
        print(f"[!] Configuration file is not a valid JSON: {file_path}")
        return None


def save_configuration(config_data, file_path):
    try:
        # config_name eksikse dosya adından belirle
        if "config_name" not in config_data:
            config_data["config_name"] = os.path.splitext(os.path.basename(file_path))[0]

        with open(file_path, 'w') as file:
            json.dump(config_data, file, indent=4)

        print(f"[✓] Configuration saved to {file_path}")
    except Exception as e:
        print(f"[!] Failed to save configuration: {e}")


def list_config_files(config_dir="configs"):
    """Return list of available .json config files in the given directory."""
    if not os.path.exists(config_dir):
        os.makedirs(config_dir)
    return [f for f in os.listdir(config_dir) if f.endswith(".json")]
