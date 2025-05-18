import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.filedialog as fd
from core.configuration import save_configuration, load_configuration, POPULAR_LANGUAGES, list_config_files
import os
import json
from shutil import which
import zipfile
import sv_ttk
FONT = ("Segoe UI", 11)
BG_COLOR = "#f4f4f4"
BTN_COLOR = "#dcdcdc"
ACCENT_COLOR = "#4CAF50"
HOVER_COLOR = "#c0c0c0"


def setup_styles():
    sv_ttk.set_theme("light")  # Sadece bu yeterli

    style = ttk.Style()
    style.configure("Green.TButton",
                    foreground="white",
                    background="#388e3c",
                    font=("Segoe UI", 10, "bold"),
                    padding=10)
    style.map("Green.TButton",
              background=[("active", "#2e7d32"), ("pressed", "#1b5e20")])
    style.configure("TButton", font=("Segoe UI", 11), padding=8)
    style.map("TButton",
              background=[("active", HOVER_COLOR)],
              relief=[("pressed", "sunken"), ("!pressed", "flat")])
    style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"))
    style.configure("Treeview", font=("Segoe UI", 11), rowheight=30)

class IAEApp(tk.Tk):

    def __init__(self):
        super().__init__()  # Tk penceresi önce oluşturulmalı

        import sv_ttk
        sv_ttk.set_theme("light")  # Tema burada uygulanmalı

        setup_styles()  # Tema sonrası stiller uygulanır

        self.title("Integrated Assignment Environment (IAE)")
        self.geometry("1200x700")
        self.configure(bg=BG_COLOR)
        self._create_menu()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.nav_frame = tk.Frame(self, width=200, bg="#e0e0e0")
        self.nav_frame.grid(row=0, column=0, sticky="ns")

        self.container = tk.Frame(self, bg="blue", width=800, height=600)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.pack_propagate(False)

        self.frames = {}
        for F in (ProjectFrame, ConfigFrame, TestFrame):
            name = F.__name__.replace("Frame", "")
            frame = F(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.place(relwidth=1, relheight=1)

        buttons = {"Project": "Project", "Configuration": "Config", "Test": "Test"}
        for label, frame_name in buttons.items():
            btn = ttk.Button(self.nav_frame, text=label, command=lambda n=frame_name: self.show_frame(n))
            btn.pack(pady=30, fill="x", padx=20)

        self.show_frame("Project")
        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_close(self):
        self.destroy()
        import sys
        sys.exit()

    def _create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Manual", command=self._show_manual)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _show_manual(self):
        manual_window = tk.Toplevel(self)
        manual_window.title("User Manual")
        manual_window.geometry("650x550")
        manual_window.configure(bg="#f5f5f5")

        manual_text = tk.Text(manual_window, wrap="word", font=FONT)
        manual_text.pack(expand=True, fill="both", padx=10, pady=10)

        manual_text.insert("1.0", """Welcome to the Integrated Assignment Environment (IAE)!

    ➤ PROJECT TAB
- Enter a project name and select a configuration.
- Choose the folder containing student ZIP submissions.
- Provide input and expected output text files.
- Save the project setup or load an existing one.
- Folder selection opens a ZIP extraction window.

➤ CONFIGURATION TAB
- Add, edit, or delete configurations.
- Define language, compile and run commands.
- Set input type (Standard Input / Command-line Arguments) via dropdown.
- Each configuration is saved as a JSON file.

➤ TEST TAB
- Select a project and run tests for all students.
- Results are displayed in a table (compile/run/status).
- Outputs are compared against expected results automatically.

TIPS:
- Input and expected output are plain .txt files.
- Configurations are reusable, editable JSONs.
- Python-like languages don’t need compile commands (leave empty).
""")
        manual_text.configure(state="disabled")

    def _show_about(self):
        messagebox.showinfo("About", "Integrated Assignment Environment (IAE) v1.0\n\nDeveloped as part of CE316 Project\n\nFeatures:\n- Project and Configuration Management\n- Automatic Testing of Student Submissions\n- JSON-based Save & Load\n")

    def show_frame(self, name):
        self.frames[name].tkraise()


class ProjectFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)

        tk.Label(self, text="Project Page", font=("Caveat", 22), bg=BG_COLOR).pack(pady=20)
        self.entries = {}
        labels = [
            ("Project Name", "project_name"),
            ("Select Config File", "config_file"),
            ("Folder Path", "zip_folder"),
            ("Input File (Optional)", "input_file"),
            ("Expected Output File", "expected_output")
        ]

        for text, key in labels:
            row = tk.Frame(self, bg=BG_COLOR)
            row.pack(fill="x", padx=20, pady=8)

            tk.Label(row, text=text, font=FONT, bg=BG_COLOR, width=20, anchor="e").pack(side="left")

            if key == "config_file":
                combo = ttk.Combobox(row, width=20, state="readonly")
                combo['values'] = list_config_files("configs")
                combo.pack(side="left", padx=10)
                self.entries[key] = combo
                combo.bind("<Button-1>", lambda e: combo.configure(values=list_config_files("configs")))
            elif key in ["zip_folder", "input_file", "expected_output"]:
                if key == "zip_folder":
                    btn = ttk.Button(row, text="Select Folder", command=lambda k=key: self.select_file(k), width=50)
                    btn.pack(side="left", padx=10)
                else:
                    btn = ttk.Button(row, text="Select File", command=lambda k=key: self.select_file(k), width=50)
                    btn.pack(side="left", padx=10)

                self.entries[key] = btn
            else:
                entry = ttk.Entry(row, width=20)
                entry.pack(side="left", padx=10)
                self.entries[key] = entry

        btn_row = tk.Frame(self, bg=BG_COLOR)
        btn_row.pack(pady=20)
        ttk.Button(btn_row, text="Save Project", command=self.save_project).pack(side="left", padx=10)
        ttk.Button(btn_row, text="Load Project", command=self.load_project).pack(side="left", padx=10)

    def save_project(self):
        project_data = {
            "project_name": self.entries["project_name"].get(),
            "config_file": self.entries["config_file"].get(),
            "zip_folder": self.entries["zip_folder"].cget("text"),
            "input_file": self.entries["input_file"].cget("text"),
            "expected_output_file": self.entries["expected_output"].cget("text")
        }
        test_frame = self.master.master.frames.get("Test")
        if test_frame and hasattr(test_frame, "results"):
            project_data["results"] = test_frame.results
        file_path = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], title="Save Project As")
        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump(project_data, f, indent=4)
                messagebox.showinfo("Saved", f"Project saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save project:\n{e}")

    def load_project(self):
        file_path = fd.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")], title="Open Project File")
        if file_path:
            try:
                with open(file_path, "r") as f:
                    project_data = json.load(f)
                self.entries["project_name"].delete(0, tk.END)
                self.entries["project_name"].insert(0, project_data.get("project_name", ""))
                self.entries["config_file"].delete(0, tk.END)
                self.entries["config_file"].insert(0, project_data.get("config_file", ""))
                self.entries["zip_folder"].config(text=project_data.get("zip_folder", "Select Folder"))
                self.entries["input_file"].config(text=project_data.get("input_file", "Select File"))
                self.entries["expected_output"].config(text=project_data.get("expected_output_file", "Select File"))
                messagebox.showinfo("Loaded", f"Project loaded from:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project:\n{e}")

    def select_file(self, key):
        if key != "zip_folder":
            file_path = fd.askopenfilename(title=f"Select {key.replace('_', ' ').capitalize()} File")
            if file_path:
                self.entries[key].config(text=file_path)
            return

        popup = tk.Toplevel(self)
        popup.title("Select ZIP Folder and Extraction Folder")
        popup.geometry("400x200")
        popup.resizable(False, False)

        selected_zip_dir = tk.StringVar(value="Not selected")
        selected_extract_dir = tk.StringVar(value="Not selected")

        def browse_zip_folder():
            path = fd.askdirectory(title="Select Folder Containing ZIP Files")
            if path:
                selected_zip_dir.set(path)

        def browse_extract_folder():
            path = fd.askdirectory(title="Select Folder to Extract ZIP Files Into")
            if path:
                selected_extract_dir.set(path)

        def extract_and_close():
            zip_dir = selected_zip_dir.get()
            extract_root = selected_extract_dir.get()

            if not os.path.isdir(zip_dir) or not os.path.isdir(extract_root):
                messagebox.showerror("Error", "Please select both folders.")
                return

            zip_files = [f for f in os.listdir(zip_dir) if f.lower().endswith(".zip")]
            if not zip_files:
                messagebox.showwarning("No ZIP Files", "No ZIP files found in the selected folder.")
                return

            for zip_name in zip_files:
                zip_path = os.path.join(zip_dir, zip_name)
                extract_to = os.path.join(extract_root, os.path.splitext(zip_name)[0])
                os.makedirs(extract_to, exist_ok=True)
                try:
                    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
                        zip_ref.extractall(extract_to)
                except Exception as e:
                    messagebox.showerror("Extraction Failed", f"Failed to extract {zip_name}:\n{e}")

            self.entries[key].config(text=extract_root)
            popup.destroy()

        # UI düzeni
        popup.columnconfigure(0, weight=1)
        popup.columnconfigure(1, weight=2)

        tk.Label(popup, text="ZIP folder:").grid(row=0, column=0, padx=10, pady=15, sticky="e")
        tk.Button(popup, text="Browse ZIP Folder", command=browse_zip_folder) \
            .grid(row=0, column=1, padx=10, ipadx=20, sticky="ew")

        tk.Label(popup, text="Extract to:").grid(row=1, column=0, padx=10, pady=15, sticky="e")
        tk.Button(popup, text="Browse Output Folder", command=browse_extract_folder) \
            .grid(row=1, column=1, padx=10, ipadx=20, sticky="ew")

        ttk.Button(popup, text="Extract and Confirm",
                   command=extract_and_close).grid(row=2, column=0, columnspan=2, pady=30, ipadx=40, padx=20, sticky="ew")


class ConfigFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.selected_language = tk.StringVar()
        tk.Label(self, text="Configuration", font=("Caveat", 22), bg=BG_COLOR).pack(pady=20)

        self.language_listbox = tk.Listbox(
            self,
            font=FONT,
            width=30,
            height=8,
            bg="#eeeeee",
            fg="#000000",
            selectbackground="#d0eaff",
            selectforeground="#000000",
            bd=2,
            relief="ridge",
            highlightthickness=1,
            highlightbackground="black",
            highlightcolor="#cccccc",
            activestyle='none'
        )

        self.language_listbox.pack(pady=20)
        self.language_listbox.bind("<<ListboxSelect>>", self.on_language_select)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add New Configuration", command=self.show_add_config_page).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Edit Selected", command=self.edit_selected_config).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Selected", command=self.delete_selected_config).pack(side="left", padx=5)

        self.detail_frame = tk.Frame(self, bg=BG_COLOR)
        self.detail_frame.pack(pady=20)

        self.populate_language_list()


    def populate_language_list(self):
        self.language_listbox.delete(0, tk.END)
        if not os.path.exists("configs"):
            os.makedirs("configs")
        for filename in os.listdir("configs"):
            if filename.endswith(".json"):
                name = os.path.splitext(filename)[0]
                self.language_listbox.insert(tk.END, name)

    def on_language_select(self, event):
        selection = self.language_listbox.curselection()
        if not selection:
            return
        config_name = self.language_listbox.get(selection[0])
        path = os.path.join("configs", f"{config_name}.json")
        config = load_configuration(path)
        self.show_config_details(config)

    def show_config_details(self, config):
        for widget in self.detail_frame.winfo_children():
            widget.destroy()
        if not config:
            return
        ttk.Label(self.detail_frame, text=f"Language: {config.get('language', '')}", font=FONT, background=BG_COLOR).pack(pady=5)
        ttk.Label(self.detail_frame, text=f"Compile: {config.get('compile_command', '')}", font=FONT, background=BG_COLOR).pack(pady=5)
        ttk.Label(self.detail_frame, text=f"Run: {config.get('run_command', '')}", font=FONT, background=BG_COLOR).pack(pady=5)
        ttk.Label(self.detail_frame, text=f"Input Type: {config.get('input_type', '')}", font=FONT, background=BG_COLOR).pack(pady=5)

    def show_add_config_page(self):
        AddConfigWindow(self)

    def edit_selected_config(self):
        selection = self.language_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a configuration to edit.")
            return
        config_name = self.language_listbox.get(selection[0])
        path = os.path.join("configs", f"{config_name}.json")
        config = load_configuration(path)
        if config:
            AddConfigWindow(self, existing_config=config, original_name=config_name)

    def delete_selected_config(self):
        selection = self.language_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a language to delete.")
            return
        config_name = self.language_listbox.get(selection[0])
        path = os.path.join("configs", f"{config_name}.json")
        if messagebox.askyesno("Delete", f"Are you sure you want to delete the configuration for {config_name}?"):
            try:
                os.remove(path)
                self.populate_language_list()
                for widget in self.detail_frame.winfo_children():
                    widget.destroy()
                messagebox.showinfo("Deleted", f"{config_name} configuration deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete configuration: {e}")


class AddConfigWindow(tk.Toplevel):
    def __init__(self, master, existing_config=None, original_name=None):
        super().__init__(master)
        self.title("Edit Configuration" if existing_config else "Add New Configuration")
        self.geometry("500x450")
        self.master = master
        self.configure(bg=BG_COLOR)
        self.original_name = original_name

        self.entries = {}
        row = tk.Frame(self, bg=BG_COLOR)
        row.pack(pady=10, padx=20, anchor="w")
        tk.Label(row, text="Language:", font=FONT, bg=BG_COLOR, width=18, anchor="e").pack(side="left")
        self.language_combo = ttk.Combobox(row, values=list(POPULAR_LANGUAGES.keys()), font=FONT, width=30)
        self.language_combo.pack(side="left")
        if existing_config:
            self.language_combo.set(existing_config.get("language", ""))
            self.language_combo.config(state="disabled")
        else:
            self.language_combo.bind("<<ComboboxSelected>>", self.autofill_fields)

        row = tk.Frame(self, bg=BG_COLOR)
        row.pack(pady=10, padx=20, anchor="w")
        tk.Label(row, text="Config Name:", font=FONT, bg=BG_COLOR, width=18, anchor="e").pack(side="left")
        self.name_entry = ttk.Entry(row, width=40)
        self.name_entry.pack(side="left")
        if existing_config and original_name:
            self.name_entry.insert(0, original_name)

        for key in ["compile_command", "run_command", "input_type"]:
            row = tk.Frame(self, bg=BG_COLOR)
            row.pack(pady=10, padx=20, anchor="w")
            label = key.replace("_", " ").title()
            tk.Label(row, text=f"{label}:", font=FONT, bg=BG_COLOR, width=18, anchor="e").pack(side="left")
            if key == "input_type":
                entry = ttk.Combobox(row, values=["Command-line Arguments", "Standard Input","None"], font=FONT, width=38)
                entry.set("Command-line Arguments")
            else:
                entry = ttk.Entry(row, width=40)
            entry.pack(side="left")
            self.entries[key] = entry

        if existing_config:
            for key in self.entries:
                value = existing_config.get(key, "")
                if isinstance(self.entries[key], ttk.Combobox):
                    self.entries[key].set(value)
                else:
                    self.entries[key].insert(0, value)

        ttk.Button(self, text="Save Configuration", command=self.save_new_config).pack(pady=20)

    def autofill_fields(self, event):
        lang = self.language_combo.get()
        if lang in POPULAR_LANGUAGES:
            config = POPULAR_LANGUAGES[lang]
            for key, val in config.items():
                if key in self.entries:
                    self.entries[key].delete(0, tk.END)
                    self.entries[key].insert(0, val)

    def save_new_config(self):
        language = self.language_combo.get()
        config_name = self.name_entry.get().strip()
        if not language or not config_name:
            messagebox.showerror("Missing Info", "Please select a language and enter a config name.")
            return

        data = {"language": language}
        for key in self.entries:
            data[key] = self.entries[key].get()
        for cmd in [data['compile_command'], data['run_command']]:
            if cmd.strip():
                first_word = cmd.strip().split()[0]
                if which(first_word) is None:
                    self.show_tool_error(first_word)
                    return

        data.update({"input_file": "", "expected_output_file": "", "compare_command": "diff output.txt expected.txt"})
        safe_name = config_name.lower().replace(" ", "_")
        file_path = os.path.join("configs", f"{safe_name}.json")
        if self.original_name and self.original_name.lower() != safe_name:
            try:
                os.remove(os.path.join("configs", f"{self.original_name.lower()}.json"))
            except FileNotFoundError:
                pass
        save_configuration(data, file_path)
        self.master.populate_language_list()
        messagebox.showinfo("Saved", f"Configuration saved as {file_path}")
        self.destroy()

    def show_tool_error(self, tool):
        help_message = (
            f"The command '{tool}' could not be found on your system.\n\n"
            f"Possible reasons:\n"
            f"• The tool is not installed.\n"
            f"• It is installed but not added to your system PATH.\n\n"
            f"🔧 Solution:\n"
            f"→ Make sure '{tool}' is installed and accessible from the terminal or command prompt.\n"
            f"→ You can test this by typing '{tool}' in a terminal.\n\n"
            f"Example for Windows (GCC):\n  Add C:\\MinGW\\bin to your Environment Variables > PATH.\n\n"
            f"Example for macOS/Linux (Java):\n  Add export PATH=$PATH:/usr/bin/java to your shell config.\n"
        )
        messagebox.showerror("Missing Tool", help_message)

class TestFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.project_data = {}
        self.results = []

        tk.Label(self, text="Test", font=("Caveat", 22), bg=BG_COLOR).pack(pady=20)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Select Project", command=self.load_project_file).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Run All Tests", command=self.run_all_tests).pack(side="left", padx=5)

        columns = ("student_id", "compile_status", "run_status", "result")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=20)

        style = ttk.Style()
        style.configure("Treeview.Heading", font=(FONT[0], 11, "bold"))
        style.configure("Treeview", font=FONT, rowheight=30)

        for col in columns:
            self.tree.heading(col, text=col.replace("_", " ").title())
            self.tree.column(col, width=200, anchor="center")

        self.tree.pack(padx=20, pady=10, fill="both", expand=True)

    def load_project_file(self):
        file_path = fd.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")], title="Select Project File")
        if file_path:
            try:
                with open(file_path, "r") as f:
                    self.project_data = json.load(f)

                student_dir = self.project_data.get("zip_folder")
                if not student_dir or not os.path.isdir(student_dir):
                    messagebox.showwarning("Invalid Folder", "Student folder path in the project file is missing or invalid.")
                    return

                self.project_data["student_code_dir"] = student_dir

                messagebox.showinfo("Loaded", f"Project loaded:\n{file_path}\n\nStudent codes from:\n{student_dir}")

            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project:{e}")

    def run_all_tests(self):
        if not self.project_data.get("config_file") or not self.project_data.get("student_code_dir"):
            messagebox.showwarning("Missing Data", "Please load a project file and student codes first.")
            return

        from core.executor import run_all_submissions

        config_path = self.project_data["config_file"]
        if not os.path.isfile(config_path):
            config_path = os.path.join("configs", config_path)
            if not os.path.isfile(config_path):
                messagebox.showerror("Configuration Error", f"Configuration file not found:\n{config_path}")
                return
            self.project_data["config_file"] = config_path

        results = run_all_submissions(self.project_data)
        self.results = results

        for item in self.tree.get_children():
            self.tree.delete(item)

        for student_id, compile_status, run_status, result in results:
            self.tree.insert("", "end", values=(student_id, compile_status, run_status, result))


if __name__ == "__main__":
    app = IAEApp()
    app.mainloop()
