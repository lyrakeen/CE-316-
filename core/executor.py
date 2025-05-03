import subprocess
from core.configuration import load_configuration
import os

def compile_code(compile_command, working_dir=None):
    try:
        result = subprocess.run(
            compile_command,
            shell=True,
            cwd=working_dir,  # >>> burası kritik
            capture_output=True,
            text=True
        )
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

def run_executable(run_command, input_file=None, output_file=None, working_dir=None):
    try:
        with open(input_file, 'r') if input_file else None as inp, \
             open(output_file, 'w') if output_file else None as out:

            result = subprocess.run(
                run_command,
                shell=True,
                stdin=inp,
                stdout=out,
                stderr=subprocess.PIPE,
                text=True,
                cwd=working_dir  # BURASI KRİTİK
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

def normalize_output(path):
    with open(path, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines()]
        return [line for line in lines if line]

def run_all_submissions(project_data):
    config = load_configuration(project_data["config_file"])
    student_dir = project_data["student_code_dir"]
    input_file = project_data.get("input_file", None)
    expected_file = project_data.get("expected_output_file", None)

    results = []

    for student_root in os.listdir(student_dir):
        student_path = os.path.join(student_dir, student_root)
        if not os.path.isdir(student_path):
            continue

        main_file = None
        for root, _, files in os.walk(student_path):
            for f in files:
                ext_map = {
                    "Python": ".py",
                    "Java": ".java",
                    "C": ".c",
                    "C++": ".cpp"
                }
                lang_ext = ext_map.get(config.get("language", ""), "").lower()

                if f.lower() == f"main{lang_ext}":
                    main_file = os.path.join(root, f)
                    break
            if main_file:
                break

        if not main_file:
            results.append((student_root, "-", "-", "main file not found"))
            continue

        exec_name = os.path.join(student_path, f"{student_root}_exec")

        compile_cmd = config["compile_command"].replace("{source}", main_file).replace("{output}", exec_name).strip()
        if compile_cmd:
            comp_ok, _ = compile_code(compile_cmd, working_dir=os.path.dirname(main_file))
            compile_status = "OK" if comp_ok else "Error"
        else:
            compile_status = "N/A"
            comp_ok = True

        if not comp_ok:
            results.append((student_root, compile_status, "-", "Compile Failed"))
            continue

        output_path = os.path.join(student_path, f"{student_root}_output.txt")
        run_cmd = config["run_command"].replace("{exec}", exec_name).strip()

        if config.get("input_type") == "Command-line Arguments" and input_file:
            try:
                with open(input_file, "r") as f:
                    args = f.read().strip()
                run_cmd = f"{run_cmd} {args}"
                input_for_run = None
            except Exception:
                input_for_run = None
        else:
            input_for_run = input_file

        run_ok, _ = run_executable(
            run_cmd,
            input_file=input_for_run,
            output_file=output_path,
            working_dir=os.path.dirname(main_file)
        )
        run_status = "OK" if run_ok else "Error"

        if not run_ok:
            results.append((student_root, compile_status, run_status, "Runtime Failed"))
            continue

        compare_cmd = config.get("compare_command", "").strip()
        if compare_cmd:
            compare_cmd = compare_cmd.replace("actual.txt", output_path).replace("expected.txt", expected_file)
            try:
                result_obj = subprocess.run(compare_cmd, shell=True, capture_output=True, text=True)
                result = "Passed" if result_obj.returncode == 0 else "Wrong Output"
            except Exception:
                result = "Compare Error"
        else:
            try:
                actual_lines = normalize_output(output_path)
                expected_lines = normalize_output(expected_file)
                if actual_lines == expected_lines:
                    result = "Passed"
                else:
                    print("[DEBUG] Actual:", actual_lines)
                    print("[DEBUG] Expected:", expected_lines)
                    result = "Wrong Output"
            except Exception as e:
                print(f"[!] File comparison error: {e}")
                result = "Compare Error"

        results.append((student_root, compile_status, run_status, result))

    return results



