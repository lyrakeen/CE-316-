import customtkinter as ctk
import tkinter.filedialog as fd
import tkinter as tk
from tkinter import messagebox
import os
import json
from core.configuration import save_configuration, load_configuration

ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

FONT = ("Segoe UI", 11)

class IAEApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Integrated Assignment Environment (IAE)")
        self.geometry("1200x700")

        self._create_menu()

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.nav_frame = ctk.CTkFrame(self, width=200, fg_color="#e0e0e0")
        self.nav_frame.grid(row=0, column=0, sticky="ns")
        self.nav_frame.grid_rowconfigure('all', weight=1)

        self.container = ctk.CTkFrame(self)
        self.container.grid(row=0, column=1, sticky="nsew")

        self.frames = {}
        for F in (ProjectFrame, ConfigFrame, TestFrame):
            name = F.__name__.replace("Frame", "")
            frame = F(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.place(relwidth=1, relheight=1)

        buttons = {
            "Project": "Project",
            "Configuration": "Config",
            "Test": "Test"
        }

        for i, (label, frame_name) in enumerate(buttons.items()):
            self.nav_frame.grid_rowconfigure(i, weight=1)
            btn = ctk.CTkButton(self.nav_frame, text=label, font=("Segoe UI", 14), height=60,
                                command=lambda n=frame_name: self.show_frame(n))
            btn.grid(row=i, column=0, padx=20, pady=10, sticky="ew")

        self.show_frame("Project")

    def _create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project", command=lambda: messagebox.showinfo("File", "New Project clicked"))
        file_menu.add_command(label="Open", command=lambda: messagebox.showinfo("File", "Open clicked"))
        file_menu.add_command(label="Save", command=lambda: messagebox.showinfo("File", "Save clicked"))
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Manual", command=self._show_manual)
        help_menu.add_command(label="About", command=lambda: messagebox.showinfo("About", "IAE v1.0"))
        menubar.add_cascade(label="Help", menu=help_menu)

        self.configure(menu=menubar)

    def _show_manual(self):
        manual_window = tk.Toplevel(self)
        manual_window.title("User Manual")
        manual_window.geometry("600x500")

        manual_text = tk.Text(manual_window, wrap="word", font=("Segoe UI", 11))
        manual_text.pack(expand=True, fill="both", padx=10, pady=10)

        manual_text.insert("1.0", """Welcome to the Integrated Assignment Environment (IAE)!

This guide will help you understand how to use the application step by step.

1. PROJECT TAB
- Enter a project name.
- Select a configuration JSON file (or create one from the Configuration tab).
- Choose the folder containing student ZIP submissions.
- Specify the input file and expected output file.

2. CONFIGURATION TAB
- Choose a language: C, Java, or Python.
- Enter the compile and run commands.
- Specify how input will be passed (arguments or stdin).
- Click 'Save Configuration' to export a JSON file.

3. TEST TAB
- Click 'Run All Tests' to start processing all student submissions.
- The table will display compile status, runtime result, and final comparison.
- Results are shown in real-time.

TIPS:
- Use 'File > Save' to store the current project setup.
- You can open saved projects from 'File > Open'.
- For help or updates, check the 'About' section.
""")

        manual_text.configure(state="disabled")

    def show_frame(self, name):
        self.frames[name].tkraise()

class ProjectFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkLabel(self, text="Project Page", font=("Arial", 16)).pack(pady=20)

        self.entries = {}
        labels = [
            ("Project Name", "project_name"),
            ("Select Config File", "config_file"),
            ("ZIP Folder", "zip_folder"),
            ("Input File", "input_file"),
            ("Expected Output File", "expected_output")
        ]

        for text, key in labels:
            row = ctk.CTkFrame(self)
            row.pack(fill="x", padx=40, pady=8)

            ctk.CTkLabel(row, text=text, font=FONT, width=180, anchor="e").pack(side="left")
            entry = ctk.CTkEntry(row, width=300)
            entry.pack(side="left", padx=10)
            self.entries[key] = entry

        btn_row = ctk.CTkFrame(self)
        btn_row.pack(pady=20)

        ctk.CTkButton(btn_row, text="Save Project", command=self.save_project).pack(side="left", padx=10)
        ctk.CTkButton(btn_row, text="Load Project", command=self.load_project).pack(side="left", padx=10)

    def save_project(self):
        data = {k: self.entries[k].get() for k in self.entries}
        file_path = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump(data, f, indent=4)
                messagebox.showinfo("Saved", f"Project saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def load_project(self):
        file_path = fd.askopenfilename(defaultextension=".json", filetypes=[("JSON Files", "*.json")])
        if file_path:
            try:
                with open(file_path, "r") as f:
                    data = json.load(f)
                for key in self.entries:
                    self.entries[key].delete(0, "end")
                    self.entries[key].insert(0, data.get(key, ""))
                messagebox.showinfo("Loaded", f"Project loaded from:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", str(e))

class ConfigFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        wrapper = ctk.CTkFrame(self)
        wrapper.pack(pady=40)

        ctk.CTkLabel(wrapper, text="Language", font=FONT).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.language_combo = ctk.CTkComboBox(wrapper, values=["C", "Java", "Python"], font=FONT)
        self.language_combo.grid(row=0, column=1, padx=10, pady=10)

        ctk.CTkLabel(wrapper, text="Compile Command", font=FONT).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.compile_entry = ctk.CTkEntry(wrapper, width=300)
        self.compile_entry.grid(row=1, column=1, padx=10, pady=10)

        ctk.CTkLabel(wrapper, text="Run Command", font=FONT).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.run_entry = ctk.CTkEntry(wrapper, width=300)
        self.run_entry.grid(row=2, column=1, padx=10, pady=10)

        ctk.CTkLabel(wrapper, text="Input Type", font=FONT).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.input_type_combo = ctk.CTkComboBox(wrapper, values=["Command-line Arguments", "Standard Input"], font=FONT)
        self.input_type_combo.grid(row=3, column=1, padx=10, pady=10)

        btn_row = ctk.CTkFrame(wrapper)
        btn_row.grid(row=4, column=1, pady=20, sticky="e")

        ctk.CTkButton(btn_row, text="Save Configuration", command=self.save_config).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="Load Configuration", command=self.load_config).pack(side="left", padx=5)
        ctk.CTkButton(btn_row, text="Delete Configuration", command=self.delete_config).pack(side="left", padx=5)

    def save_config(self):
        data = {
            "language": self.language_combo.get(),
            "compile_command": self.compile_entry.get(),
            "run_command": self.run_entry.get(),
            "input_type": self.input_type_combo.get(),
            "input_file": "",
            "expected_output_file": "",
            "compare_command": "diff output.txt expected.txt"
        }
        file_path = fd.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            save_configuration(data, file_path)
            messagebox.showinfo("Saved", f"Configuration saved to:\n{file_path}")

    def load_config(self):
        file_path = fd.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            data = load_configuration(file_path)
            if data:
                self.language_combo.set(data.get("language", ""))
                self.compile_entry.delete(0, "end")
                self.compile_entry.insert(0, data.get("compile_command", ""))
                self.run_entry.delete(0, "end")
                self.run_entry.insert(0, data.get("run_command", ""))
                self.input_type_combo.set(data.get("input_type", ""))
                messagebox.showinfo("Loaded", f"Configuration loaded from:\n{file_path}")

    def delete_config(self):
        file_path = fd.askopenfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this file?\n\n{file_path}")
            if confirm:
                try:
                    os.remove(file_path)
                    messagebox.showinfo("Deleted", f"Deleted:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file:\n{e}")

class TestFrame(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)

        ctk.CTkButton(self, text="Run All Tests").pack(pady=20)

        headers = ["Student ID", "Compile Status", "Run Status", "Result"]
        data = [
            ["20230001", "Success", "Success", "Passed"],
            ["20230002", "Error", "N/A", "Failed"]
        ]

        table_frame = ctk.CTkFrame(self)
        table_frame.pack(padx=20, pady=10, fill="both", expand=True)

        for col_index, header in enumerate(headers):
            label = ctk.CTkLabel(table_frame, text=header, font=(FONT[0], 11, "bold"), anchor="center")
            label.grid(row=0, column=col_index, padx=10, pady=5, sticky="nsew")
            table_frame.grid_columnconfigure(col_index, weight=1)

        for row_index, row_data in enumerate(data, start=1):
            for col_index, cell in enumerate(row_data):
                label = ctk.CTkLabel(table_frame, text=cell, font=FONT, anchor="center")
                label.grid(row=row_index, column=col_index, padx=10, pady=5, sticky="nsew")

if __name__ == "__main__":
    app = IAEApp()
    app.mainloop()
