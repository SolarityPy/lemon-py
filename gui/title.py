from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage, CTkOptionMenu
import tkinter as tk
from functools import partial

class Title:
    def __init__(self, root):
        self.root = root

    def title_bar_setup(self):
        title_pane = CTkFrame(self.root, width=2, height=25, corner_radius=0, fg_color="#1A1919")
        title_pane.grid(row=0, column=0, columnspan=4, sticky="new")

        title_pane.bind("<Button-1>", self.start_drag)
        title_pane.bind("<B1-Motion>", self.drag)
        title_pane.bind("<ButtonRelease-1>", self.end_drag)
        
        title_options = {
            "Lemon": {
                "type": "CTkLabel",
                "color": "#FFBF00",
                "direction": "left"
            },

            "File": {
                "type": "CTkButton",
                "color": "#FFFFFF",
                "direction": "left",
                "dropdown": {
                    "Open Configuration": {
                        "command": lambda: self.open_button_handler()
                    },

                    "Save Config": {
                        "command": "pass" # do later
                    }
                }
            },

            "Settings": {
                "type": "CTkButton",
                "color": "#FFFFFF",
                "direction": "left",
                "dropdown": {
                    "placeholder": {
                        "command": "placeholder"
                    }
                }
            },

            "Help": {
                "type": "CTkButton",
                "color": "#FFFFFF",
                "command": "",
                "direction": "left",
                "dropdown": {
                    "placeholder": {
                        "command": "placeholder"
                    }
                }
            },

            "—": {
                "type": "CTkButton",
                "color": "#F0F0F0",
                "command": self.root.quit,
                "direction": "right"
            }
        }
        
        for i, (name, attributes) in enumerate(title_options.items()):
            ctk_type = globals()[attributes['type']]
            
            if attributes['type'] == "CTkLabel":
                option = ctk_type(title_pane, text=name, font=("Arial", 16, "bold"), 
                                text_color=attributes['color'])
                option.pack(side=attributes['direction'], padx=8)
                
            elif attributes['type'] == "CTkButton":
                if "dropdown" in attributes:
                    option = ctk_type(title_pane, text=name, font=("Arial", 12, "bold"), text_color=attributes['color'], fg_color="transparent", 
                                hover_color="#333333", command=partial(self.create_dropdown, option, attributes), corner_radius=0, width=30, height=15)
                else:
                    option = ctk_type(title_pane, text=name, font=("Arial", 12, "bold"), text_color=attributes['color'], fg_color="transparent", 
                                hover_color="#333333", command=attributes.get('command', ''), corner_radius=0, width=30, height=15)
                
                
                option.pack(side=attributes['direction'], padx=1)

    def create_dropdown(self, option, attributes):
        dropdown_menu = tk.Menu(self.root, tearoff=0)
        if 'dropdown' in attributes.keys():
            for options in attributes['dropdown']:
                dropdown_menu.add_command(label=options, command=attributes['dropdown'][options]['command'])
        
        #dropdown_frame.grid(row=y_position+1, column=x_position)
        x = option.winfo_rootx() + (self.root.winfo_width() // 11)
        # "to lemon or not to lemon"
        #               - Rishabh

        y = option.winfo_rooty() + option.winfo_height()

        # Post the menu at that position
        dropdown_menu.tk_popup(x, y)
        

    def start_drag(self, event):
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        
    def drag(self, event):
        dx = event.x_root - self.drag_start_x
        dy = event.y_root - self.drag_start_y
        

        current_x = self.root.winfo_x()
        current_y = self.root.winfo_y()
        
        new_x = current_x + dx
        new_y = current_y + dy
        self.root.geometry(f"+{new_x}+{new_y}")
        
        self.drag_start_x = event.x_root
        self.drag_start_y = event.y_root
        
    def end_drag(self, event):
        # Reset drag variables (optional)
        self.drag_start_x = 0
        self.drag_start_y = 0