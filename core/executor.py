import subprocess
from contextlib import nullcontext
from core.configuration import load_configuration
import os
import json
def compile_code(compile_command, cwd=None):
    try:
        result = subprocess.run(compile_command, shell=True, capture_output=True, text=True, cwd=cwd)
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

def run_executable(run_command, input_type="Standard Input", input_file=None, cli_arguments="", output_file=None, cwd=None):
    """
    Executes the program based on input method:
    - If Standard Input: passes input_file as stdin
    - If Command-line Arguments: appends cli_arguments to the run command
    - If None: runs the command with no input
    """
    try:
        if input_type == "None":
            result = subprocess.run(
                run_command,
                shell=True,
                stdout=open(output_file, 'w') if output_file else None,
                stderr=subprocess.PIPE,
                text=True,
                cwd=cwd
            )
        else:
            inp_ctx = open(input_file, 'r') if input_type == "Standard Input" and input_file else nullcontext()
            out_ctx = open(output_file, 'w') if output_file else nullcontext()

            with inp_ctx as inp, out_ctx as out:
                result = subprocess.run(
                    run_command,
                    shell=True,
                    stdin=inp if input_type == "Standard Input" and input_file else None,
                    stdout=out if output_file else None,
                    stderr=subprocess.PIPE,
                    text=True,
                    cwd=cwd
                )

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

def run_all_submissions(config, project_data):
    student_dir = project_data["student_code_dir"]
    input_type = project_data.get("input_type", "Standard Input")
    cli_args = project_data.get("cli_arguments", "") if input_type == "Command-line Arguments" else ""
    input_file = project_data.get("input_file") if input_type == "Standard Input" else None
    expected_output_file = project_data["expected_output_file"]
    run_template = config["run_command"]
    compile_template = config["compile_command"]

    results = []

    for student_id in os.listdir(student_dir):
        student_path = os.path.join(student_dir, student_id)
        if not os.path.isdir(student_path):
            continue

       
        main_file = None
        for ext in [".py", ".c", ".cpp", ".java", ".kt", ".go", ".rb", ".js", ".rs", ".kt"]:
            for fname in os.listdir(student_path):
                if fname.endswith(ext):
                    main_file = os.path.join(student_path, fname)
                    break
            if main_file:
                break

        if not main_file:
            print(f"[!] No source file found for {student_id}")
            results.append((student_id, "Missing File", "-", "-"))
            continue

       
        compile_cmd = compile_template.replace("{main_file}", f"\"{main_file}\"")
        run_cmd = run_template.replace("{main_file}", f"\"{main_file}\"")
        if input_type == "Command-line Arguments" and cli_args.strip():
            run_cmd += " " + cli_args.strip()

        print(f"[>] Running for {student_id}: {run_cmd}")

       
        success, compile_log = compile_code(compile_cmd, cwd=student_path)
        if not success:
            print(f"[✗] {student_id}: Compile Failed")
            results.append((student_id, "Compile Failed", "-", "-"))
            continue

        output_file = os.path.join(student_path, "output.txt")
        success, run_log = run_executable(run_cmd, input_type, input_file, cli_args, output_file, cwd=student_path)
        if not success:
            print(f"[✗] {student_id}: Runtime Error")
            results.append((student_id, "Compiled", "Runtime Error", "-"))
            continue

      
        try:
            with open(output_file, 'r') as out_f, open(expected_output_file, 'r') as exp_f:
                student_output = out_f.read().strip()
                expected_output = exp_f.read().strip()
                if student_output == expected_output:
                    print(f"[✓] {student_id}: Passed")
                    results.append((student_id, "Compiled", "Executed", "Passed"))
                else:
                    print(f"[✗] {student_id}: Wrong Output")
                    results.append((student_id, "Compiled", "Executed", "Wrong Output"))
        except Exception as e:
            print(f"[!] Output Comparison Error: {e}")
            results.append((student_id, "Compiled", "Executed", "Output Error"))

    print("\n[!] Note: Make sure to use '{main_file}' in your config file for full compatibility.")
    return results


def save_results_to_project(project_path, results):
    try:
        with open(project_path, 'r') as f:
            project_data = json.load(f)

        project_data["results"] = results

        with open(project_path, 'w') as f:
            json.dump(project_data, f, indent=4)

        print("[✓] Results saved to project file.")
    except Exception as e:
        print(f"[✗] Failed to save results: {e}")

def normalize_output(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
        return [line for line in lines if line]
