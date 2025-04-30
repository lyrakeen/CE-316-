import subprocess

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
