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
  