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
    
    def create_hub(self, conf_dic):
        root = self.root
        
        self.init()
        root.grid_columnconfigure(0, weight=6000)   # Left pane 
        root.grid_columnconfigure(1, weight=18000)  # Right side 
        root.grid_rowconfigure(0, weight=1)      # Full height
        
        left_pane = CTkFrame(root, border_width=5)
        left_pane.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")
        self.fill_left_pane(left_pane, conf_dic)
        
        # Change padx to fill the gap completely
        right_pane = CTkFrame(root, border_width=5)
        right_pane.grid(row=0, column=1, padx=(2, 5), pady=5, sticky="nsew")

        '''
        forensics_
        apps_button = CTkButton(root, "Required Applications")
        gp_button = CTkButton(root, "Group Policy")
        '''
    
    def fill_left_pane(self, pane, conf_dic):
        pane.grid_columnconfigure(0, weight=1)

        conf_name = CTkLabel(pane, text=f"{conf_dic['name']}", font=("Arial", 16, "bold"), wraplength=100, justify="left")
        conf_name.grid(row=0, column=0, padx=10, pady=(10, 0), sticky="nw")

        checks = conf_dic['check']
        total_vulns = len(checks)
        total_points = sum(check['points'] for check in checks)

        conf_points = CTkLabel(pane, text=f"{total_points}pts", font=("Arial", 16, "bold"), wraplength=100, justify="left")
        conf_points.grid(row=1, column=0, padx=10, pady=(20, 0), sticky="nw")

        total_vulns = CTkLabel(pane, text=f"{total_vulns} vulns.", font=("Arial", 16, "bold"), wraplength=100, justify="left")
        total_vulns.grid(row=2, column=0, padx=10, pady=(0, 5), sticky="nw")

        conf_os = CTkLabel(pane, text=f"OS: {conf_dic['os'].title()}", font=("Arial", 16, "bold"), wraplength=100, justify="left")
        conf_os.grid(row=3, column=0, padx=10, pady=(20, 5), sticky="nw")

        conf_user = CTkLabel(pane, text=f"User: {conf_dic['user']}", font=("Arial", 16, "bold"), wraplength=100, justify="left")
        conf_user.grid(row=4, column=0, padx=10, pady=(20, 5), sticky="nw")

        try:
            conf_remote = CTkLabel(pane, text=f"Remote: {conf_dic['remote']}", font=("Arial", 16, "bold"), wraplength=100, justify="left")
            conf_remote.grid(row=5, column=0, padx=10, pady=(20, 0), sticky="nw")
        except:
            conf_local = CTkLabel(pane, text="Local Scoring", font=("Arial", 16, "bold"), wraplength=100, justify="left")
            conf_local.grid(row=5, column=0, padx=10, pady=(20, 0), sticky="nw")