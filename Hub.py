from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage
from PIL import Image
from Resolve import Resolve

class Hub:
    def __init__(self, root, command_objects_list, resolve_answers=None):
        self.root = root
        self.command_objects_list = command_objects_list
        self.resolve_answers = resolve_answers
        
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def init(self): # 7/24
        self.root.geometry("650x450")
        self.clear_screen()
    
    def create_hub(self, conf_dic):
        self.conf_dic = conf_dic
        root = self.root
        
        self.init()
        root.grid_columnconfigure(0, weight=7000)   # Left pane 
        root.grid_columnconfigure(1, weight=0)  # Border column, no expansion
        root.grid_columnconfigure(2, weight=17000)  # Right side 
        root.grid_rowconfigure(0, weight=1)      # Full height
        
        # Create a thin frame to act as the border
        left_border = CTkFrame(root, width=2, fg_color="#444444")  # Choose your border color
        left_border.grid(row=0, column=1, sticky="ns")  # Place it between left and right panes

        # Main left pane, no border
        left_pane = CTkFrame(root, border_width=0)
        left_pane.grid(row=0, column=0, sticky="nsew")
        self.fill_left_pane(left_pane, conf_dic)
        
        # Main right pane, no border
        right_pane = CTkFrame(root, border_width=0)
        right_pane.grid(row=0, column=2, sticky="nsew")
        self.fill_right_pane(right_pane, root)

        '''
        forensics_
        apps_button = CTkButton(root, "Required Applications")
        gp_button = CTkButton(root, "Group Policy")
        '''
    
    def fill_left_pane(self, pane, conf_dic):
        pane.grid_columnconfigure(0, weight=1)

        conf_name = CTkLabel(pane, text=f"{conf_dic['name']}", font=("Arial", 16, "bold"), wraplength=150, justify="left")
        conf_name.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        checks = conf_dic['check']
        total_vulns = len(checks)
        total_points = sum(check['points'] for check in checks)

        conf_points = CTkLabel(pane, text=f"{total_points}pts", font=("Arial", 16, "bold"), wraplength=100, justify="left")
        conf_points.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="nw")

        total_vulns = CTkLabel(pane, text=f"{total_vulns} vulnerabilities", font=("Arial", 16, "bold"), wraplength=150, justify="left")
        total_vulns.grid(row=2, column=0, padx=10, pady=(0, 0), sticky="nw")

        conf_os = CTkLabel(pane, text=f"OS: {conf_dic['os'].title()}", font=("Arial", 16, "bold"), wraplength=150, justify="left")
        conf_os.grid(row=3, column=0, padx=10, pady=(25, 0), sticky="nw")

        conf_user = CTkLabel(pane, text=f"User: {conf_dic['user']}", font=("Arial", 16, "bold"), wraplength=100, justify="left")
        conf_user.grid(row=4, column=0, padx=10, pady=(25, 0), sticky="nw")

        try:
            conf_remote = CTkLabel(pane, text=f"Remote: {conf_dic['remote']}", font=("Arial", 16, "bold"), wraplength=150, justify="left")
            conf_remote.grid(row=5, column=0, padx=10, pady=(25, 0), sticky="nw")
        except:
            conf_local = CTkLabel(pane, text="Local Scoring", font=("Arial", 16, "bold"), wraplength=100, justify="left")
            conf_local.grid(row=5, column=0, padx=10, pady=(25, 0), sticky="nw")

    def fill_right_pane(self, pane, root):
        pane.grid_columnconfigure(0, weight=1)
        pane.grid_columnconfigure(1, weight=1)

        buttons_data = [
            {"btn": "put here", "command": ""},
            {"btn": "put here", "command": ""},
            {"btn": "put here", "command": ""},
            {"btn": "put here", "command": ""},
            {"btn": "put here", "command": ""},
            {"btn": "put here", "command": ""},
            {"btn": "put here", "command": ""},
            {"btn": "put here", "command": ""}
        ]
        for i, btn_data in enumerate(buttons_data):
            button = CTkButton(pane, text=btn_data["btn"], command=btn_data["command"], height=45, font=("Arial", 16, "bold"))
            button.grid(row=i//2, column=i%2, padx=10, pady=10, sticky="new")

        resolve_btn = CTkButton(pane, text="Resolve", command=lambda: self.open_resolve_mode(), height=60, font=("Bahnschrift", 20, "bold"), fg_color="#A00E1A", hover_color="#860A0A")
        resolve_btn.grid(row=4, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        build_btn = CTkButton(pane, text="Build", command="", height=80, font=("Bahnschrift", 20, "bold"))
        build_btn.grid(row=5, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

    def open_resolve_mode(self):
        #callback function that restores hub
        def hub_callback(resolve_answers):
            self.clear_screen()
            self.resolve_answers = resolve_answers
            self.create_hub(self.conf_dic) # recreate hub
        
        # Pass this callback to Resolve
        resolve = Resolve(self.root, self.command_objects_list, hub_callback, self.resolve_answers)
        resolve.resolve()
