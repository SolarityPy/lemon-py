import subprocess, os, requests
from Command import Command
from Prompt import Prompt

class Commands:
    def __init__(self, root):
        self.root = root
    # === COMPLEX COMMAND FUNCTIONS ===

    def user_detail_command(self,p, not_boolean):
        if p['key'].lower() == "fullname" :
            return Command(f"net user '{p['user']}' /fullname:\"\"")
        
        elif p['key'].lower() == "isenabled":
            # not_boolean indicates Not type (ex. UserDetailNot)
            if not_boolean:
                if p['value'].lower() == "yes":
                    return Command(f"net user '{p['user']}' /active:yes")
                else:
                    return Command(f"net user '{p['user']}' /active:no")
            else: # Normal condition
                if p['value'].lower() == "yes":
                    return Command(f"net user '{p['user']}' /active:no")
                else:
                    return Command(f"net user '{p['user']}' /active:yes")
            
        elif p['key'].lower() == "isadmin":
            if not_boolean:
                if p['value'].lower() == "yes":
                    return Command(f"net localgroup Administrators '{p['user']}' /add")
                else:
                    return Command(f"net localgroup Administrators '{p['user']}' /delete")
            else:
                if p['value'].lower() == "yes":
                    return Command(f"net localgroup Administrators '{p['user']}' /delete")
                else:
                    return Command(f"net localgroup Administrators '{p['user']}' /add")
        
        elif p['key'].lower() == "passwordneverexpires":
            if not_boolean:
                if p['value'].lower() == "yes":
                    return Command(f"WMIC USERACCOUNT WHERE Name='{p['user']}' SET PasswordExpires=TRUE") 
                else:
                    return Command(f"WMIC USERACCOUNT WHERE Name='{p['user']}' SET PasswordExpires=FALSE")
            else:
                if p['value'].lower() == "yes":
                    return Command(f"WMIC USERACCOUNT WHERE Name='{p['user']}' SET PasswordExpires=FALSE")
                else:
                    return Command(f"WMIC USERACCOUNT WHERE Name='{p['user']}' SET PasswordExpires=TRUE")
                
        elif p['key'].lower() == "nopasswordchange":
            if not_boolean:
                if p['value'].lower() == "yes":
                    return Command(f"net user '{p['user']}' /PasswordChg:Yes")
                else:
                    return Command(f"net user '{p['user']}' /PasswordChg:No")
            else:
                if p['value'].lower() == "yes":
                    return Command(f"net user '{p['user']}' /PasswordChg:No")
                else:
                    return Command(f"net user '{p['user']}' /PasswordChg:Yes")
    

    def download(self, path, url):
        r = requests.get(url)
        if r.status_code == 200:
            with open(path, 'wb') as file:
                file.write(r.content)
                return True
        else:
            return None    
        

    def share_exists_command(self, p, not_boolean):
        if not_boolean:
            path = Prompt(self.root, ["What path would you like the share to broadcast?"]).question_prompt()
            
            return Command(f"net share {p['name']}={path}") # create a new share
        else:
            return Command(f"net share {p['name']} /delete") # delete the share
        

    def program_installed_command(self, p, not_boolean): # In the future, Lemon will ask the user for any required programs: Lemon will use this check as penalty
        program_list = {
            "FireFox": {
                "extension": "msi",
                "latest": r"https://download.mozilla.org/?product=firefox-msi-latest-ssl&os=win64&lang=en-US&attribution_code=c291cmNlPXN1cHBvcnQubW96aWxsYS5vcmcmbWVkaXVtPXJlZmVycmFsJmNhbXBhaWduPShub3Qgc2V0KSZjb250ZW50PShub3Qgc2V0KSZleHBlcmltZW50PShub3Qgc2V0KSZ2YXJpYXRpb249KG5vdCBzZXQpJnVhPWVkZ2UmY2xpZW50X2lkX2dhND01MDEzNzE4NDguMTc0OTAwNDc0MyZzZXNzaW9uX2lkPTc3MjMwNTMyODQmZGxzb3VyY2U9bW96b3Jn&attribution_sig=7ba90acf45f025ea79b153fc3f23cd0c46d921bbcc0dbcf340eb123d007103ae&_gl=1*1w7f5lo*_ga*NTAxMzcxODQ4LjE3NDkwMDQ3NDM.*_ga_MQ7767QQQW*czE3NDkwMDQ3NDMkbzEkZzEkdDE3NDkwMDQ4NzYkajQ3JGwwJGgw",
                "old": r"https://ftp.mozilla.org/pub/firefox/releases/106.0b3/win64/en-US/Firefox%20Setup%20106.0b3.msi",
                "old_version": "106.0b3"
            },

            "CCleaner": {
                "extemsion" : "msi",
                "latest" : r"https://www.ccleaner.com/go/get_ccbe_msi",
                "old": r"", #find later
                "old_version": ""
            },

            "Notepad++": {
                "extemsion" : "msi",
                "latest" : r"",
                "old": r"", #find later
                "old_version": ""
            }
        }

        desired_program = Prompt(self.root, program_list).click_disired_prompt()
    '''
            choice = input(f"Latest version of {p['name']}? (y/n: installs old)")
            Prompt(self.root).prompt()
            
            if choice.lower() == "y": old_version = False 
            else: old_version = True
            
            for program in program_list.keys():
                if p['name'].lower() in program or program in p['name'].lower:
                    download_url = program_list[program]["latest" if not old_version else "old"]
                    extension = program_list[program]['extension']
                    
                    file_name = f"{program}.{extension}"
                    if Commands.download(file_name, download_url):
                        if extension == "msi":
                            return Command(file_name + " /qn")
            pass
    '''
    commands = {
        # === USER COMMANDS ===
        # Note: https://www.tenforums.com/attachments/tutorial-test/142289d1499096195-change-user-rights-assignment-security-policy-settings-windows-10-a-ntrights.zip
        # Only way to change user rights assignment is to use this program, first dependency :(
            
        "userexists": lambda self, p: Command(f"net user {p['name']} /delete"),
        "userexistsnot": lambda self, p: Command(f"net user {p['name']} CyberPatriots1! /add"),
        
        "userdetail": lambda self, p, not_boolean: self.user_detail_command(p, not_boolean),
        "userdetailnot": lambda self, p, not_boolean: self.user_detail_command(p, not_boolean),
        
        "useringroup": lambda self, p: Command(f"net localgroup '{p['group']}' '{p['user']}' /delete"),
        "useringroupnot": lambda self, p: Command(f"net localgroup '{p['group']}' '{p['user']}' /add"),
        
        "userrights": lambda self, p: Command(f"ntrights -r {p['value']} -u {p['name']}"),
        "userrightsnot": lambda self, p: Command(f"ntrights +r {p['value']} -u {p['name']}"),
        
        # === SECURITY COMMANDS ===
        "firewallup": lambda self, p: Command("netsh advfirewall set allprofiles state off"),
        "firewallupnot": lambda self, p: Command("netsh advfirewall set allprofiles state on"),
        
        # === WINDOWS FEATURES ===
        "windowsfeature": lambda self, p: Command(f"Dism /Online /Disable-Feature /FeatureName:{p['name']}"),
        "windowsfeaturenot": lambda self, p: Command(f"Dism /Online /Enable-Feature /FeatureName:{p['name']}"),
        
        # === SERVICES ===
        "serviceup": lambda self, p: Command(f"sc stop '{p['name']}'"),
        "serviceupnot": lambda self, p: Command(f"sc start '{p['name']}'"),

        "servicestartup": lambda self, p: Command(f"sc config '{p['name']}' start='{"disabled" if p['startup'] == 'automatic' else 'auto'}'"),
        "servicestartupnot": lambda self, p: Command(f"sc config '{p['name']}' start='{"auto" if p['startup'] == 'automatic' else 'disabled'}'"),
        
        "programinstalled": lambda self, p, not_boolean: self.program_installed_command(p, not_boolean),
        "programinstallednot": lambda self, p, not_boolean: self.program_installed_command(p, not_boolean),

        # === MISCELLANEOUS ===
        "shareexists": lambda self, p, not_boolean: self.share_exists_command(p, not_boolean),
        "shareexistsnot": lambda self, p, not_boolean: self.share_exists_command(p, not_boolean)
    }
