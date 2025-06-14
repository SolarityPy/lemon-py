from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage, CTkOptionMenu
import tkinter as tk
from tkinter import filedialog
from Translator import Translator
from ConfigParser import ConfigParser
from PIL import Image
from gui.Build import Build
from gui.Resolve import Resolve
from tkinter import messagebox
from functools import partial
from gui.EditCommands import EditCommands
from gui.title import Title

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

        title = Title(self.root)
        title.title_bar_setup()

        self.content_setup()

        self.bottom_bar_setup()
    
    def bottom_bar_setup(self):
        bottom_pane = CTkFrame(self.root, width=2, height=35, corner_radius=0, fg_color="#1A1919")
        bottom_pane.grid(row=4, column=0, columnspan=4, sticky="sew")

        edit_button = CTkButton(bottom_pane, text="Edit", font=("Arial", 18, "bold"), text_color="#FFFFFF",
                                command=self.open_edit_mode, width=30, height=30, fg_color="#B58C0E", hover_color="#93720D")
        edit_button.pack(side="left", padx=(4,4), pady=(4,4))

        hammer_image = Image.open(r"assets\hammer.png")  
        hammer_ctk_image = CTkImage(hammer_image, size=(24, 24))

        build_button = CTkButton(bottom_pane, image=hammer_ctk_image, text="",
                            command=self.open_build_mode, width=30, height=30,
                                fg_color="#B58C0E", hover_color="#93720D")
        build_button.pack(side="right", padx=(4,4), pady=(4,4))

        self.is_resolved = True
        for command_obj in self.command_objects_list:
            if "#" in command_obj.get_command():
                self.is_resolved = False
        if self.is_resolved:
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
        self.root.update_idletasks()
        
        translator_object = Translator(config_dictionary, self)
        command_objects_list = translator_object.translate()
                    
        # Iterate through all Command objects and pass in any required questions to the hub
        
        self.create_hub(config_dictionary)
        
        # Force layout recalculation
        self.root.update_idletasks()

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
        if not self.is_resolved:
            messagebox.showerror(title="Cannot Build", message="Please resolve all commands before building!")
            return
        build = Build(self.command_objects_list, hub_callback)
        build.build_exe()