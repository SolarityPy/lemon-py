from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame
class Prompt:
    def __init__(self, root, prompts):
        self.root = root
        self.prompts = prompts
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def prep_prompt(self):
        # Prepping for the prompt
        self.root.geometry("600x400")
        self.clear_screen()
        
        self.root.title("Lemon - Prompt")
    def question_prompt(self):
        self.prep_prompt()
        for i in range(len(self.prompts)):
            if isinstance(self.prompts[i], str):
                self.root.grid_columnconfigure(i, weight=1)
                question_label = CTkLabel(self.root, text=self.prompts[i], font=("Arial", 12))
                text_entry = CTkEntry(self.root, font=("Arial", 10), height=30, width=450)
                question_label.grid(row=i, column=0, padx=20, pady=10, sticky="w")
                text_entry.grid(padx=20, pady=10, sticky="w")
    
    def click_disired_prompt(self):
        self.prep_prompt()
        for i in range(len(self.prompts.keys())):
            self.root.grid_columnconfigure(i, weight=1)