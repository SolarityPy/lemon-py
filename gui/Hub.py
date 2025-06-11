from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage, CTkOptionMenu
import tkinter as tk
from PIL import Image
from gui.Build import Build
from gui.Resolve import Resolve
from functools import partial
from gui.EditCommands import EditCommands

class Hub:
    def __init__(self, root, command_objects_list, resolve_answers=None):
        self.root = root
        self.command_objects_list = command_objects_list
        self.resolve_answers = resolve_answers
        self.drag_start_x = 0
        self.drag_start_y = 0
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def init(self):
        self.root.geometry("650x450")
        self.root.overrideredirect(True)
        self.clear_screen()
    
    def create_hub(self, conf_dic):
        self.conf_dic = conf_dic
        root = self.root
        
        self.init()


        root.rowconfigure(0, weight=0)
        root.rowconfigure(1, weight=1)
        root.rowconfigure(2, weight=0) 
        root.rowconfigure(3, weight=0) 
        root.rowconfigure(4, weight=0) 
        for i in range(4):
            root.columnconfigure(i, weight=1)

        self.title_bar_setup()

        self.content_setup()

        self.bottom_bar_setup()
    
    def bottom_bar_setup(self):
        bottom_pane = CTkFrame(self.root, width=2, height=35, corner_radius=0, fg_color="#1A1919")
        bottom_pane.grid(row=4, column=0, columnspan=4, sticky="sew")

        edit_button = CTkButton(bottom_pane, text="Edit Commands", font=("Arial", 18, "bold"), text_color="#FFFFFF",
                                command=self.open_edit_mode, width=30, height=30)
        edit_button.pack(side="left", padx=(4,4), pady=(4,4))

        hammer_image = Image.open("assets\hammer.png")  
        hammer_ctk_image = CTkImage(hammer_image, size=(24, 24))

        build_button = CTkButton(bottom_pane, image=hammer_ctk_image, text="",
                            command=self.open_build_mode, width=30, height=30, fg_color="#0070ca", 
                                hover_color="#0070ca")
        build_button.pack(side="right", padx=(4,4), pady=(4,4))

        is_resolved = True
        for command_obj in self.command_objects_list:
            if "#" in command_obj.get_command():
                is_resolved = False
        if is_resolved:
            resolve_btn = CTkButton(bottom_pane, text="Resolve", command=lambda: self.open_resolve_mode(), height=30, width=30, 
                                    font=("Bahnschrift", 20, "bold"), fg_color="#0B6626", hover_color="#0E7416")
        else:
            resolve_btn = CTkButton(bottom_pane, text="Resolve", command=lambda: self.open_resolve_mode(), width=30, height=30, 
                                    font=("Bahnschrift", 20, "bold"), fg_color="#A00E1A", hover_color="#860A0A")
        resolve_btn.pack(side="right", padx=(4,4), pady=(4,4))

    def content_setup(self):
        content_pane = CTkFrame(self.root, width=2, height=800, corner_radius=0, fg_color="#2B2929")
        content_pane.grid(row=1, column=0, rowspan=2, columnspan=4, sticky="news")

        for i in range(4):
            content_pane.columnconfigure(i, weight=1)

        conf_name = CTkLabel(content_pane, text=f"{self.conf_dic['name']}", font=("Arial", 32, "bold"), text_color="#FFBF00")
        conf_name.grid(row=0, column=0, padx=10, pady=(10,0), sticky="nw")

        conf_os = CTkLabel(content_pane, text=f"{self.conf_dic['os'].title()}", font=("Arial", 12, "bold"), text_color="#FFFFFF")
        conf_os.grid(row=1, column=0, padx=10, pady=0, sticky="nw")

        checks = self.conf_dic['check']
        total_vulns = len(checks)
        total_points = sum(check['points'] for check in checks)

        conf_points = CTkLabel(content_pane, text=f"{total_vulns} vulns, {total_points} points", font=("Arial", 16, "bold"), text_color="#FFBF00")
        conf_points.grid(row=0, column=4, padx=10, pady=(20,0), sticky="ne")

        try:
            conf_info = CTkLabel(content_pane, text=f"User: {self.conf_dic['user']}, Remote: {self.conf_dic['remote']}", font=("Arial", 12, "bold"))
            conf_info.grid(row=1, column=4, padx=10, pady=0, sticky="nw")
        except:
            conf_info = CTkLabel(content_pane, text=f"User: {self.conf_dic['user']}, Local Scoring", font=("Arial", 12, "bold"))
            conf_info.grid(row=1, column=4, padx=10, pady=0, sticky="nw")

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
                        "command": "pass"
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
        print(attributes.keys())
        if 'dropdown' in attributes.keys():
            for options in attributes['dropdown']:
                dropdown_menu.add_command(label=options)
        
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

    def open_resolve_mode(self):
        #callback function that restores hub
        def hub_callback(resolve_answers):
            self.clear_screen()
            self.resolve_answers = resolve_answers
            self.create_hub(self.conf_dic) # recreate hub
        
        # Pass this callback to Resolve
        resolve = Resolve(self.root, self.command_objects_list, hub_callback, self.resolve_answers)
        resolve.resolve()

    def open_edit_mode(self):
        def hub_callback():
            self.clear_screen()
            self.create_hub(self.conf_dic)

        edit = EditCommands(self.root, self.command_objects_list, hub_callback)
        edit.create_EditCommands()

    def open_build_mode(self):
        def hub_callback():
            self.clear_screen()
            self.create_hub(self.conf_dic)

        build = Build(self.command_objects_list, hub_callback)
        build.build_exe()