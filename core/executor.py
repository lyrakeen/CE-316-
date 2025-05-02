import subprocess
from core.configuration import load_configuration
import os

def compile_code(compile_command):
    """
    Compiles the source code using the given command string.
    Example: "gcc main.c -o main"
    """
    try:
        result = subprocess.run(compile_command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print("[✓] Compilation successful.")
            return True, result.stdout
        else:
            print("[✗] Compilation failed.")
            print(result.stderr)
            return False, result.stderr
    except Exception as e:
        print(f"[!] Compilation error: {e}")
        return False, str(e)

def run_executable(run_command, input_file=None, output_file=None):
    """
    Runs the compiled executable or script.
    You can optionally redirect input and output via file paths.
    """
    try:
        with open(input_file, 'r') if input_file else None as inp, \
             open(output_file, 'w') if output_file else None as out:

            result = subprocess.run(run_command, shell=True, stdin=inp, stdout=out, stderr=subprocess.PIPE, text=True)

        if result.returncode == 0:
            print("[✓] Execution successful.")
            return True, None
        else:
            print("[✗] Execution failed.")
            print(result.stderr)
            return False, result.stderr
    except Exception as e:
        print(f"[!] Execution error: {e}")
        return False, str(e)

def run_all_submissions(project_data):
    config_path = os.path.join("configs", project_data["config_file"])
    config = load_configuration(config_path)
    student_dir = project_data["student_code_dir"]
    input_file = project_data.get("input_file", None)
    expected_file = project_data.get("expected_output_file", None)

    results = []

    for file_name in os.listdir(student_dir):
        if file_name.endswith(config["language"][:2].lower()):  # py, ja, c
            student_id = os.path.splitext(file_name)[0]
            source_path = os.path.join(student_dir, file_name)
            exec_name = os.path.join(student_dir, f"{student_id}_exec")

            # Compile
            # === Compile aşaması ===
            if config["language"].lower() != "python":
                compile_cmd = config["compile_command"].replace("{source}", source_path).replace("{output}", exec_name)
                comp_ok, _ = compile_code(compile_cmd)
                if not comp_ok:
                    results.append((student_id, "Error", "-", "Compile Failed"))
                    continue
            else:
                comp_ok = True  # Python için compile yok, otomatik geç

            if not comp_ok:
                results.append((student_id, "Error", "-", "Compile Failed"))
                continue

            # Run
            output_path = os.path.join(student_dir, f"{student_id}_output.txt")
            if config["language"].lower() == "Python":
                run_cmd = config["run_command"].replace("{exec}", source_path)
            else:
                run_cmd = config["run_command"].replace("{exec}", exec_name)

            run_ok, _ = run_executable(run_cmd, input_file=input_file, output_file=output_path)

            if not run_ok:
                results.append((student_id, "Success", "Error", "Runtime Failed"))
                continue

            # Compare
            with open(output_path, "r") as act, open(expected_file, "r") as exp:
                actual = act.read().strip()
                expected = exp.read().strip()
                result = "Passed" if actual == expected else "Wrong Output"

            results.append((student_id, "Success", "Success", result))

    return results
