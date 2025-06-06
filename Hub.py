from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage
from PIL import Image

class Hub:
    def __init__(self, root):
        self.root = root
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def init(self): # 7/24
        self.root.geometry("650x450")
        self.clear_screen()
    
    def create_buttons(self):
        root = self.root
        
        self.init()
        root.grid_columnconfigure(0, weight=6)   # Left pane - 7/24 of width
        root.grid_columnconfigure(1, weight=18)  # Right side - 17/24 of width
        root.grid_rowconfigure(0, weight=1)      # Full height
        
        left_pane = CTkFrame(root, border_width=5)
        left_pane.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        
        # Change padx to fill the gap completely
        right_pane = CTkFrame(root, border_width=5)
        right_pane.grid(row=0, column=1, padx=(2, 5), pady=5, sticky="nsew")

        '''
        forensics_
        apps_button = CTkButton(root, "Required Applications")
        gp_button = CTkButton(root, "Group Policy")
        '''
