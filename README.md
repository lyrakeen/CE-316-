# Integrated Assignment Environment (IAE)

IAE is a user-friendly assignment evaluation tool for lecturers. It allows batch testing of student code submissions using custom configurations.

## 💡 Features
- Create, edit, delete custom configurations for different languages (Java, Python, Ruby etc.)
- Supports both **standard input** and **command-line arguments**
- Load student submissions from a folder
- Automatically compiles and runs submissions
- Displays compile/run status and result (output match)
- Saves projects for later use
- Editable configurations for multi-class languages (e.g. Java)

## Project Flow

1. **Project Tab**:  
   - Enter a project name  
   - Select a configuration (`.json` format)  
   - Choose student ZIP folder  
   - Attach input and expected output files  
   - Save or load project

2. **Configuration Tab**:  
   - Create new configs or edit existing ones  
   - Fill in compile/run commands manually or auto-fill by language  
   - Choose input method (Standard Input / Command-line Arguments)

3. **Test Tab**:  
   - Select project and click **Run All Tests**  
   - See real-time compile/run results and correctness check

## 📁 Notes
- All configurations are saved under `/configs` as JSON
- Project settings are stored in `.json` files  
- Input/output files are separate `.txt` files provided by the user

## Example Commands
**Java**  
Compile: `javac Main.java`  
Run: `java Main`

**Python**  
Compile: *(leave empty)*  
Run: `python3 main.py`

---

> This project is building as part of CE316 coursework.
