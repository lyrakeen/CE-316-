import tkinter as tk
from tkinter import ttk, messagebox

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

        # Frame sınıfları ve isimleri eşleşiyor
        self.frames = {}
        for F in (ProjectFrame, ConfigFrame, TestFrame):
            name = F.__name__.replace("Frame", "")  # 'Project', 'Config', 'Test'
            frame = F(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.place(relwidth=1, relheight=1)

        # Menü butonları: görünen isim → frame ismi
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

    def _show_about(self):
        messagebox.showinfo("About", "Integrated Assignment Environment v1.0")

    def show_frame(self, name):
        self.frames[name].tkraise()

# === Project Section ===
class ProjectFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)

        tk.Label(self, text="Project Page", font=("Arial", 16), bg=BG_COLOR).pack(pady=20)

        labels = ["Project Name", "Select Config File", "ZIP Folder", "Input File", "Expected Output File"]
        for text in labels:
            row = tk.Frame(self, bg=BG_COLOR)
            row.pack(fill="x", padx=20, pady=8)

            tk.Label(row, text=text, font=FONT, bg=BG_COLOR, width=20, anchor="e").pack(side="left")
            ttk.Entry(row, width=40).pack(side="left", padx=10)

# === Configuration Section ===
class ConfigFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent, bg=BG_COLOR)
        wrapper = tk.Frame(self, bg=BG_COLOR)
        wrapper.pack(pady=40, anchor="n")

        ttk.Label(wrapper, text="Language", background=BG_COLOR, font=FONT).grid(row=0, column=0, padx=10, pady=10, sticky="e")
        ttk.Combobox(wrapper, values=["C", "Java", "Python"], font=FONT, width=30).grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(wrapper, text="Compile Command", background=BG_COLOR, font=FONT).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        ttk.Entry(wrapper, width=50).grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(wrapper, text="Run Command", background=BG_COLOR, font=FONT).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        ttk.Entry(wrapper, width=50).grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(wrapper, text="Input Type", background=BG_COLOR, font=FONT).grid(row=3, column=0, padx=10, pady=10, sticky="e")
        ttk.Combobox(wrapper, values=["Command-line Arguments", "Standard Input"], font=FONT, width=30).grid(row=3, column=1, padx=10, pady=10)

        ttk.Button(wrapper, text="Save Configuration").grid(row=4, column=1, padx=10, pady=30, sticky="e")

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

# === Run App ===
if __name__ == "__main__":
    app = IAEApp()
    app.mainloop()

