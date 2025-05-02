import json

POPULAR_LANGUAGES = {
    "C": {
        "compile_command": "gcc main.c -o main",
        "run_command": "./main",
        "input_type": "Standard Input"
    },
    "C++": {
        "compile_command": "g++ main.cpp -o main",
        "run_command": "./main",
        "input_type": "Standard Input"
    },
    "Java": {
        "compile_command": "javac Main.java",
        "run_command": "java Main",
        "input_type": "Standard Input"
    },
    "Python": {
        "compile_command": "python3 -m py_compile main.py",
        "run_command": "python3 main.py",
        "input_type": "Standard Input"
    },
    "Go": {
        "compile_command": "go build main.go",
        "run_command": "./main",
        "input_type": "Standard Input"
    },
    "Ruby": {
        "compile_command": "ruby -c main.rb",
        "run_command": "ruby main.rb",
        "input_type": "Standard Input"
    },
    "Node.js": {
        "compile_command": "node --check main.js",
        "run_command": "node main.js",
        "input_type": "Standard Input"
    },
    "Rust": {
        "compile_command": "rustc main.rs",
        "run_command": "./main",
        "input_type": "Standard Input"
    },
    "Kotlin": {
        "compile_command": "kotlinc main.kt -include-runtime -d main.jar",
        "run_command": "java -jar main.jar",
        "input_type": "Standard Input"
    }
}
def load_configuration(file_path):
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
    try:
        with open(file_path, 'w') as file:
            json.dump(config_data, file, indent=4)
        print(f"[✓] Configuration saved to {file_path}")
    except Exception as e:
        print(f"[!] Failed to save configuration: {e}")
