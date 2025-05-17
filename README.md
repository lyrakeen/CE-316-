# Integrated Assignment Environment (IAE)

IAE is a simple but powerful tool to evaluate programming assignments in bulk.  
It allows lecturers to compile, run, and test student submissions via custom configurations.

## 💡 Features
- Project-based assignment management
- Multi-language configurations (C, Java, Python, etc.)
- Command-line arguments & standard input support
- Batch processing of student ZIP submissions
- Real-time result table (compile, run, compare status)
- Config edit/delete and multi-config support per language
- Input/Output file handling with .txt files


## 🧪 How It Works

### Project Tab
- Define project name, select a config, input/output files and submission folder.
- ZIP folder selection triggers extraction process.
- Save/load your project state as JSON.

### Configuration Tab
- Create new configurations or edit existing ones.
- Compile and run commands are flexible per language.
- Input Type can be 'Standard Input' or 'Command-line Arguments' via dropdown.
- Configs saved in `/configs` as JSON.

### Test Tab
- Load project and run tests on all student submissions.
- Results are displayed instantly (compile/run/output match).
- Supports languages that require multiple class files (Java) as well as interpreted languages (Python).

## 📁 Folder Structure
- `/configs`: Configuration files (.json)
- `/student_submissions`: Folder with ZIPs
- Input/output files: Provided as `.txt`

## 📝 Example Commands
**Java**  
Compile: `javac *.java`  
Run: `java MainClass`

**Python**  
Compile: *(leave empty)*  
Run: `python main.py`


---


> This project is building as part of CE316 coursework.
