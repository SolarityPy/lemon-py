import customtkinter as ctk

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
        print("button click")


app = App()
app.mainloop()