import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.filedialog as fd
from core.configuration import save_configuration
from core.configuration import save_configuration, load_configuration
import tkinter.filedialog as fd
import os
from tkinter import messagebox
import json
from shutil import which
FONT = ("Segoe UI", 11)
BG_COLOR = "#f4f4f4"
BTN_COLOR = "#dcdcdc"
ACCENT_COLOR = "#4CAF50"
HOVER_COLOR = "#c0c0c0"

class IAEApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Integrated Assignment Environment (IAE)")
        self.geometry("1200x700")
        self.configure(bg=BG_COLOR)

        self._create_menu()

        style = ttk.Style(self)
        style.configure("TButton", font=FONT, padding=8)
        style.map("TButton",
                  background=[("active", HOVER_COLOR)],
                  relief=[("pressed", "sunken"), ("!pressed", "flat")])

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.nav_frame = tk.Frame(self, width=200, bg="#e0e0e0")
        self.nav_frame.grid(row=0, column=0, sticky="ns")

        self.container = tk.Frame(self, bg="blue", width=800, height=600)
        self.container.grid(row=0, column=1, sticky="nsew")
        self.container.pack_propagate(False)


        self.frames = {}
        for F in (ProjectFrame, ConfigFrame, TestFrame):
            name = F.__name__.replace("Frame", "")  # 'Project', 'Config', 'Test'
            frame = F(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.place(relwidth=1, relheight=1)

        buttons = {
            "Project": "Project",
            "Configuration": "Config",
            "Test": "Test"
        }

        for label, frame_name in buttons.items():
            btn = ttk.Button(self.nav_frame, text=label, command=lambda n=frame_name: self.show_frame(n))
            btn.pack(pady=30, fill="x", padx=20)

        self.show_frame("Project")

    def _create_menu(self):
        menubar = tk.Menu(self)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="New Project", command=self._not_implemented)
        file_menu.add_command(label="Open", command=self._not_implemented)
        file_menu.add_command(label="Save", command=self._not_implemented)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.quit)
        menubar.add_cascade(label="File", menu=file_menu)

        help_menu = tk.Menu(menubar, tearoff=0)
        help_menu.add_command(label="User Manual", command=self._show_manual)
        help_menu.add_command(label="About", command=self._show_about)
        menubar.add_cascade(label="Help", menu=help_menu)

        self.config(menu=menubar)

    def _not_implemented(self):
        messagebox.showinfo("Not Implemented", "This feature is not yet implemented.")

    def _show_manual(self):
        manual_window = tk.Toplevel(self)
        manual_window.title("User Manual")
        manual_window.geometry("600x500")

        manual_text = tk.Text(manual_window, wrap="word", font=("Segoe UI", 11))
        manual_text.pack(expand=True, fill="both", padx=10, pady=10)

        manual_text.insert("1.0", """Welcome to the Integrated Assignment Environment (IAE)!

        Here’s a simple guide to help you get started:

        ➤ PROJECT TAB
        - Fill in project name, config file path, ZIP folder, input and expected output files.
        - Use 'Save Project' to store your setup as a JSON file.
        - Load a previous setup anytime with 'Load Project'.

        ➤ CONFIGURATION TAB
        - Choose a language and enter compile/run commands.
        - Set how input is passed (arguments or standard input).
        - Use 'Save Configuration' to create a config file.
        - 'Load' and 'Delete' help manage existing config files.

        ➤ TEST TAB
        - Click 'Run All Tests' to compile and run student submissions.
        - Results (compile/run/status) are shown in a table instantly.

        TIPS:
        - Everything is saved as simple JSON files.
        - Use the tab buttons — File menu options are not yet active.
        - Check the About section for version info.
        """)

        manual_text.configure(state="disabled")

    def _show_about(self):
        messagebox.showinfo("About", "Integrated Assignment Environment v1.0")

    def show_frame(self, name):
        self.frames[name].tkraise()



# === Project Section ===

class ProjectFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)

        tk.Label(self, text="Project Page", font=("Arial", 16), bg=BG_COLOR).pack(pady=20)

        self.entries = {}

        labels = [
            ("Project Name", "project_name"),
            ("Select Config File", "config_file"),
            ("ZIP Folder", "zip_folder"),
            ("Input File", "input_file"),
            ("Expected Output File", "expected_output")
        ]

        for text, key in labels:
            row = tk.Frame(self, bg=BG_COLOR)
            row.pack(fill="x", padx=20, pady=8)

            tk.Label(row, text=text, font=FONT, bg=BG_COLOR, width=20, anchor="e").pack(side="left")
            entry = ttk.Entry(row, width=40)
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
            "zip_folder": self.entries["zip_folder"].get(),
            "input_file": self.entries["input_file"].get(),
            "expected_output_file": self.entries["expected_output"].get()
        }

        file_path = fd.asksaveasfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Save Project As"
        )

        if file_path:
            try:
                with open(file_path, "w") as f:
                    json.dump(project_data, f, indent=4)
                messagebox.showinfo("Saved", f"Project saved to:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save project:\n{e}")

    def load_project(self):
        file_path = fd.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON Files", "*.json")],
            title="Open Project File"
        )

        if file_path:
            try:
                with open(file_path, "r") as f:
                    project_data = json.load(f)

                self.entries["project_name"].delete(0, tk.END)
                self.entries["project_name"].insert(0, project_data.get("project_name", ""))

                self.entries["config_file"].delete(0, tk.END)
                self.entries["config_file"].insert(0, project_data.get("config_file", ""))

                self.entries["zip_folder"].delete(0, tk.END)
                self.entries["zip_folder"].insert(0, project_data.get("zip_folder", ""))

                self.entries["input_file"].delete(0, tk.END)
                self.entries["input_file"].insert(0, project_data.get("input_file", ""))

                self.entries["expected_output"].delete(0, tk.END)
                self.entries["expected_output"].insert(0, project_data.get("expected_output_file", ""))

                messagebox.showinfo("Loaded", f"Project loaded from:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project:\n{e}")




class ConfigFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        wrapper = tk.Frame(self, bg=BG_COLOR)
        wrapper.pack(pady=40, anchor="n")


        ttk.Label(wrapper, text="Language", background=BG_COLOR, font=FONT).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.language_combo = ttk.Combobox(wrapper, values=["C", "Java", "Python"], font=FONT, width=30)
        self.language_combo.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(wrapper, text="Compile Command", background=BG_COLOR, font=FONT).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.compile_entry = ttk.Entry(wrapper, width=50)
        self.compile_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(wrapper, text="Run Command", background=BG_COLOR, font=FONT).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.run_entry = ttk.Entry(wrapper, width=50)
        self.run_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(wrapper, text="Input Type", background=BG_COLOR, font=FONT).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.input_type_combo = ttk.Combobox(wrapper, values=["Command-line Arguments", "Standard Input"], font=FONT, width=30)
        self.input_type_combo.grid(row=3, column=1, padx=10, pady=10)

        btn_frame = tk.Frame(wrapper, bg=BG_COLOR)
        btn_frame.grid(row=4, column=1, padx=10, pady=30, sticky="e")

        ttk.Button(btn_frame, text="Save Configuration", command=self.save_config).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Load Configuration", command=self.load_config).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Delete Configuration", command=self.delete_config).pack(side="left", padx=5)

    def save_config(self):
        config_data = {
            "language": self.language_combo.get(),
            "compile_command": self.compile_entry.get(),
            "run_command": self.run_entry.get(),
            "input_type": self.input_type_combo.get(),
            "input_file": "",
            "expected_output_file": "",
            "compare_command": "diff output.txt expected.txt"
        }
        language = config_data["language"].strip().lower()

        if not language:
            messagebox.showerror("Error", "Please select a language.")
            return

         # configs klasörünü oluştur (yoksa)
        os.makedirs("configs", exist_ok=True)

        # Örn: configs/java.json
        file_path = os.path.join("configs", f"{language}.json")

        save_configuration(config_data, file_path)
        messagebox.showinfo("Saved", f"Configuration saved to:\n{file_path}")
    
    def is_command_available(self,command_string):
         if not command_string.strip():
            return False
         executable = command_string.strip().split()[0]
         return which(executable) is not None

    def load_config(self):
        file_path = fd.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Load Configuration"
        )

        if file_path:
            config_data = load_configuration(file_path)
            if config_data:
                compile_cmd = config_data.get("compile_command", "")
                run_cmd = config_data.get("run_command", "")

            if not self.is_command_available(compile_cmd):
                messagebox.showerror("Missing Tool", f"The compiler in this config ('{compile_cmd}') is not available on this system.")
                return
            if not self.is_command_available(run_cmd):
                messagebox.showerror("Missing Tool", f"The runtime command ('{run_cmd}') is not available on this system.")
                return
           
            self.language_combo.set(config_data.get("language", ""))
            self.compile_entry.delete(0, tk.END)
            self.compile_entry.insert(0, config_data.get("compile_command", ""))
            self.run_entry.delete(0, tk.END)
            self.run_entry.insert(0, config_data.get("run_command", ""))
            self.input_type_combo.set(config_data.get("input_type", ""))
            messagebox.showinfo("Loaded", f"Configuration loaded from:\n{file_path}")

    def delete_config(self):
        file_path = fd.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Select Configuration to Delete"
        )

        if file_path:
            confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete this file?\n\n{file_path}")
            if confirm:
                try:
                    os.remove(file_path)
                    messagebox.showinfo("Deleted", f"Deleted:\n{file_path}")
                except Exception as e:
                    messagebox.showerror("Error", f"Could not delete file:\n{e}")

# === Test Section ===
class TestFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        ttk.Button(self, text="Run All Tests").pack(pady=20)

        columns = ("student_id", "compile_status", "run_status", "result")
        tree = ttk.Treeview(self, columns=columns, show="headings", height=20)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=(FONT[0], 11, "bold"))
        style.configure("Treeview", font=FONT, rowheight=30)

        for col in columns:
            tree.heading(col, text=col.replace("_", " ").title())
            tree.column(col, width=200, anchor="center")

        tree.insert("", "end", values=("20230001", "Success", "Success", "Passed"))
        tree.insert("", "end", values=("20230002", "Error", "N/A", "Failed"))

        tree.pack(padx=20, pady=10, fill="both", expand=True)

if __name__ == "__main__":
    app = IAEApp()
    app.mainloop()

