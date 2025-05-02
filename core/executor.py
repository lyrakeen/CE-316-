import subprocess
from configuration import load_configuration
import os

def compile_code(compile_command):
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
    config = load_configuration(project_data["config_file"])
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
            compile_cmd = config["compile_command"].replace("{source}", source_path).replace("{output}", exec_name)
            comp_ok, _ = compile_code(compile_cmd)

            if not comp_ok:
                results.append((student_id, "Error", "-", "Compile Failed"))
                continue

            # Run
            output_path = os.path.join(student_dir, f"{student_id}_output.txt")
            run_cmd = config["run_command"].replace("{exec}", exec_name)

            # REQ 7: input_type CONTROL (stdin or argüman)
            if config.get("input_type") == "Command-line Arguments" and input_file:
                try:
                    with open(input_file, "r") as f:
                        args = f.read().strip()
                    run_cmd = f"{run_cmd} {args}"  # Argümanlar komut satırına eklenir
                    input_for_run = None  # stdin will not be in use
                except Exception as e:
                    print(f"[!] Failed to read input file for arguments: {e}")
                    input_for_run = None
            else:
                input_for_run = input_file  # stdin will be used

            run_ok, _ = run_executable(run_cmd, input_file=input_for_run, output_file=output_path)

            if not run_ok:
                results.append((student_id, "Success", "Error", "Runtime Failed"))
                continue


            # Compare
            compare_cmd = config.get("compare_command", "").strip()

            if compare_cmd:
                compare_cmd = compare_cmd.replace("actual.txt", output_path).replace("expected.txt", expected_file)
                try:
                    result_obj = subprocess.run(compare_cmd, shell=True, capture_output=True, text=True)
                    result = "Passed" if result_obj.returncode == 0 else "Wrong Output"
                except Exception as e:
                    print(f"[!] Compare command error: {e}")
                    result = "Compare Error"
            else:
                # Default fallback comparison
                with open(output_path, "r") as act, open(expected_file, "r") as exp:
                    actual = act.read().strip()
                    expected = exp.read().strip()
                    result = "Passed" if actual == expected else "Wrong Output"

            results.append((student_id, "Success", "Success", result))

    return results
