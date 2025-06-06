import customtkinter as ctk
from ConfigParser import ConfigParser
from Translator import Translator
from Hub import Hub
from tkinter import filedialog

class App(ctk.CTk):
    def __init__(self):
        # Initializes window and sets attributes
        super().__init__()
        self.geometry("200x150")
        self.title("Lemon")
        
        # Gives the columns more "weight", spacing them out (kind of like an HBox?)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        # Standardized name: function_button
        self.open_button = ctk.CTkButton(self, text="Open Configuration", command=self.open_button_handler)
        self.open_button.grid(row=0, column=2, padx=20, pady=10)

    # Note the standardized name: button_name_handler
    def open_button_handler(self):
        # Limits the extensions to .conf, .txt, and .toml
        file_path = filedialog.askopenfilename(
            filetypes=[("Config files", "*.conf"), ("Text files", "*.txt"), ("TOML files", "*.toml")]
        )
        if file_path:
            self.start_screen(file_path)
            #could add alert if not correct file path

    def start_screen(self, file_path):
        config = ConfigParser(file_path)
        config_dictionary = config.parse()
        # Force window update before creating hub
        self.update_idletasks()
        
        hub = Hub(self)
        hub.create_hub(config_dictionary)
        
        # Force layout recalculation
        self.update_idletasks()

        '''
        translator_object = Translator(config_dictionary, self)
        translator_object.translate()
        '''

# Initializes main loop
app = App()
app.mainloop()