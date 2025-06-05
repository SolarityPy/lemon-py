from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage
from PIL import Image
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
        self.text_entries = []  # Store references to entry widgets
        
        for i in range(len(self.prompts)):
            if isinstance(self.prompts[i], str):
                self.root.grid_columnconfigure(0, weight=1)
                
                question_label = CTkLabel(self.root, text=self.prompts[i], font=("Arial", 12))
                text_entry = CTkEntry(self.root, font=("Arial", 10), height=30, width=450)
                
                question_label.grid(row=i*2, column=0, padx=20, pady=10, sticky="w")
                text_entry.grid(row=i*2+1, column=0, padx=20, pady=10, sticky="w")
                
                # Store reference to check later
                self.text_entries.append(text_entry)
        
        # Add submit button
        submit_button = CTkButton(self.root, text="Submit", command=self.check_entries)
        submit_button.grid(row=len(self.prompts)*2, column=0, pady=20)

    def check_entries(self):
        """Check if text has been entered in any field"""
        for i, entry in enumerate(self.text_entries):
            value = entry.get()  # Get current text
            if value.strip():  # Check if not empty (ignoring whitespace)
                print(f"Entry {i}: '{value}'")
            else:
                print(f"Entry {i} is empty")
    
    def load_image(self, program):
        #Use PIL to open image
        pil_image = Image.open(fr"assets\icons\{program}.png")
        #convert to ctk image
        ctl_image = CTkImage(pil_image, size=(48, 48))
        return ctl_image
    
    def click_disired_prompt(self):
        self.prep_prompt()
        program_list = list(self.prompts.keys())
        for i in range(len(program_list)):
            self.root.grid_columnconfigure(i, weight=1)
            program_name = program_list[i]
            program_icon = self.load_image(program_name.lower())
            program_button = CTkButton(self.root, image=program_icon, text=program_name, compound="bottom")
            program_button.grid(row=i//2, column=i%2, padx=25, pady=10)