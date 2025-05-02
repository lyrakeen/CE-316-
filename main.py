import tkinter as tk
from tkinter import ttk, messagebox
import tkinter.filedialog as fd
from core.configuration import save_configuration, load_configuration, POPULAR_LANGUAGES
from core.configuration import list_config_files
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
        messagebox.showinfo(
            "About",
            "Integrated Assignment Environment (IAE) v1.0\n\n"
            "Developed as part of CE316 Project\n"
            "\n"
            "Features:\n"
            "- Project and Configuration Management\n"
            "- Automatic Testing of Student Submissions\n"
            "- JSON-based Save & Load\n\n"
        )

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
            if key == "config_file":
                combo = ttk.Combobox(row, width=37, state="readonly")
                combo['values'] = list_config_files("configs")
                combo.pack(side="left", padx=10)
                self.entries[key] = combo
                combo.bind("<Button-1>", lambda e: combo.configure(values=list_config_files("configs")))
            else:
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

        # REQ 9: test sonuçlarını projeye dahil et
        test_frame = self.master.master.frames.get("Test")
        if test_frame and hasattr(test_frame, "results"):
            project_data["results"] = test_frame.results

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
        self.controller = controller
        self.selected_language = tk.StringVar()

        self.language_listbox = tk.Listbox(self, font=FONT, width=30, height=8)
        self.language_listbox.pack(pady=20)
        self.language_listbox.bind("<<ListboxSelect>>", self.on_language_select)

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=10)
        ttk.Button(btn_frame, text="Add New Configuration", command=self.show_add_config_page).pack(side="left", padx=5)
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
                lang = os.path.splitext(filename)[0].capitalize()
                self.language_listbox.insert(tk.END, lang)

    def on_language_select(self, event):
        selection = self.language_listbox.curselection()
        if not selection:
            return
        language = self.language_listbox.get(selection[0])
        path = os.path.join("configs", f"{language.lower()}.json")
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

    def delete_selected_config(self):
        selection = self.language_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a language to delete.")
            return

        language = self.language_listbox.get(selection[0])
        path = os.path.join("configs", f"{language.lower()}.json")


        if messagebox.askyesno("Delete", f"Are you sure you want to delete the configuration for {language}?"):
            try:
                os.remove(path)
                self.populate_language_list()
                for widget in self.detail_frame.winfo_children():
                    widget.destroy()
                messagebox.showinfo("Deleted", f"{language} configuration deleted.")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete configuration: {e}")


class AddConfigWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Add New Configuration")
        self.geometry("500x400")
        self.master = master
        self.configure(bg=BG_COLOR)

        self.entries = {}

        row = tk.Frame(self, bg=BG_COLOR)
        row.pack(pady=10, padx=20, anchor="w")
        tk.Label(row, text="Language:", font=FONT, bg=BG_COLOR, width=18, anchor="e").pack(side="left")
        from core.configuration import POPULAR_LANGUAGES
        self.language_combo = ttk.Combobox(row, values=list(POPULAR_LANGUAGES.keys()), font=FONT, width=30)
        self.language_combo.pack(side="left")
        self.language_combo.bind("<<ComboboxSelected>>", self.autofill_fields)

        for key in ["compile_command", "run_command", "input_type"]:
            row = tk.Frame(self, bg=BG_COLOR)
            row.pack(pady=10, padx=20, anchor="w")
            label = key.replace("_", " ").title()
            tk.Label(row, text=f"{label}:", font=FONT, bg=BG_COLOR, width=18, anchor="e").pack(side="left")
            entry = ttk.Entry(row, width=40)
            entry.pack(side="left")
            self.entries[key] = entry

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
        if not language:
            messagebox.showerror("Missing Info", "Please select a language.")
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
        file_path = os.path.join("configs", f"{language.strip().lower()}.json")
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
            f"Example for Windows (GCC):\n"
            f"  Add C:\\MinGW\\bin to your Environment Variables > PATH.\n\n"
            f"Example for macOS/Linux (Java):\n"
            f"  Add export PATH=$PATH:/usr/bin/java to your shell config.\n"
        )
        messagebox.showerror("Missing Tool", help_message)

        
# === Test Section ===
class TestFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        self.controller = controller
        self.project_data = {}
        self.results = []  # REQ 9 için eklendi: test sonuçlarını bellekte tut

        btn_frame = tk.Frame(self, bg=BG_COLOR)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="Select Project", command=self.load_project_file).pack(side="left", padx=5)
        ttk.Button(btn_frame, text="Load Student Codes", command=self.select_student_code_directory).pack(side="left", padx=5)
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
        file_path = fd.askopenfilename(
            defaultextension=".json",
            filetypes=[("JSON files", "*.json")],
            title="Select Project File"
        )
        if file_path:
            try:
                with open(file_path, "r") as f:
                    self.project_data = json.load(f)
                messagebox.showinfo("Loaded", f"Project loaded:\n{file_path}")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load project:\n{e}")

    def select_student_code_directory(self):
        folder_path = fd.askdirectory(title="Select Student Code Directory")
        if folder_path:
            self.project_data["student_code_dir"] = folder_path
            messagebox.showinfo("Loaded", f"Student codes loaded from:\n{folder_path}")

    def run_all_tests(self):
        if not self.project_data.get("config_file") or not self.project_data.get("student_code_dir"):
            messagebox.showwarning("Missing Data", "Please load a project file and student codes first.")
            return

        from core.executor import run_all_submissions
        results = run_all_submissions(self.project_data)
        self.results = results  # REQ 9 için test sonuçları bellekte saklanır

        for item in self.tree.get_children():
            self.tree.delete(item)

        for student_id, compile_status, run_status, result in results:
            self.tree.insert("", "end", values=(student_id, compile_status, run_status, result))



if __name__ == "__main__":
    app = IAEApp()
    app.mainloop()

