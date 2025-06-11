import customtkinter as ctk
from ConfigParser import ConfigParser
from Translator import Translator
from gui.Hub import Hub
from tkinter import filedialog

class App(ctk.CTk):
    def __init__(self):
        # Initializes window and sets attributes
        super().__init__()
        self.geometry("200x125")
        self.title("Lemon")
        
        # Gives the columns more "weight", spacing them out (kind of like an HBox?)
        for i in range(4):
            self.grid_columnconfigure(i, weight=1)

        welcome_label = ctk.CTkLabel(self, text="Welcome to Lemon!")
        self.open_button = ctk.CTkButton(self, text="Open Configuration", command=self.open_button_handler, fg_color="#B58C0E", hover_color="#93720D")
        self.open_button.grid(row=1, column=2, padx=20, pady=10)
        welcome_label.grid(row=0, column=2, padx=20, pady=10)

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
        try:
            self.root.update_idletasks()
        except:
            self.update_idletasks()
        
        translator_object = Translator(config_dictionary, self)
        command_objects_list = translator_object.translate()
                    
        # Iterate through all Command objects and pass in any required questions to the hub
        
        hub = Hub(self, command_objects_list)
        hub.create_hub(config_dictionary)
        
        # Force layout recalculation
        self.update_idletasks()

        

# Initializes main loop
app = App()
app.mainloop()