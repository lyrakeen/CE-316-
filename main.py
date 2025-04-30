from core.executor import compile_code, run_executable

compile_success, log = compile_code("gcc main.c -o main")
if compile_success:
    run_success, run_error = run_executable("./main", "input.txt", "output.txt")
