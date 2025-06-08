import subprocess, os, requests
from commands.Command import Command

class Commands:
    def __init__(self, root):
        self.root = root
        # Move the commands dictionary here as a class attribute
        self.commands = {
            # === USER COMMANDS ===
            # Note: https://www.tenforums.com/attachments/tutorial-test/142289d1499096195-change-user-rights-assignment-security-policy-settings-windows-10-a-ntrights.zip
            # Only way to change user rights assignment is to use this program, first dependency :(
                
            "userexists": lambda commands_obj, p, not_bool: Command(f"net user {p['name']} /delete"),
            "userexistsnot": lambda commands_obj, p, not_bool: Command(f"net user {p['name']} CyberPatriots1! /add"),
            
            "userdetail": lambda commands_obj, p, not_bool: self.user_detail_command(p, False),
            "userdetailnot": lambda commands_obj, p, not_bool: self.user_detail_command(p, True),
            
            "useringroup": lambda commands_obj, p, not_bool: Command(f"net localgroup '{p['group']}' '{p['user']}' /delete"),
            "useringroupnot": lambda commands_obj, p, not_bool: Command(f"net localgroup '{p['group']}' '{p['user']}' /add"),
            
            "userrights": lambda commands_obj, p, not_bool: Command(f"ntrights -r {p['value']} -u {p['name']}"),
            "userrightsnot": lambda commands_obj, p, not_bool: Command(f"ntrights +r {p['value']} -u {p['name']}"),
            
            # === SECURITY COMMANDS ===
            "firewallup": lambda commands_obj, p, not_bool: Command("netsh advfirewall set allprofiles state off"),
            "firewallupnot": lambda commands_obj, p, not_bool: Command("netsh advfirewall set allprofiles state on"),
            
            # === WINDOWS FEATURES ===
            "windowsfeature": lambda commands_obj, p, not_bool: Command(f"Dism /Online /Disable-Feature /FeatureName:{p['name']}"),
            "windowsfeaturenot": lambda commands_obj, p, not_bool: Command(f"Dism /Online /Enable-Feature /FeatureName:{p['name']}"),
            
            # === SERVICES ===
            "serviceup": lambda commands_obj, p, not_bool: Command(f"sc stop '{p['name']}'"),
            "serviceupnot": lambda commands_obj, p, not_bool: Command(f"sc start '{p['name']}'"),

            "servicestartup": lambda commands_obj, p, not_bool: Command(f"sc config '{p['name']}' start='{"disabled" if p['startup'] == 'automatic' else 'auto'}'"),
            "servicestartupnot": lambda commands_obj, p, not_bool: Command(f"sc config '{p['name']}' start='{"auto" if p['startup'] == 'automatic' else 'disabled'}'"),
            
            "programinstalled": lambda commands_obj, p, not_bool: self.program_installed_command(p, False),
            "programinstallednot": lambda commands_obj, p, not_bool: self.program_installed_command(p, True),

            # === MISCELLANEOUS ===
            "shareexists": lambda commands_obj, p, not_bool: self.share_exists_command(p, False),
            "shareexistsnot": lambda commands_obj, p, not_bool: self.share_exists_command(p, True)
        }
        
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

    def share_exists_command(self, p, not_boolean):
        if not_boolean:
            return Command(
                f"net share {p['name']}='#share_replace#' & REM share_exists", 
                prereq_required=True, 
                open_ended_questions=["What path would you like the share to broadcast?"]
            )
        else:
            return Command(f"net share {p['name']} /delete") # delete the share
        

    def program_installed_command(self, p, not_boolean):
        program_list = {
            "Firefox": {
                "extension": "msi",
                "latest": r"https://download.mozilla.org/?product=firefox-msi-latest-ssl&os=win64&lang=en-US&attribution_code=c291cmNlPXN1cHBvcnQubW96aWxsYS5vcmcmbWVkaXVtPXJlZmVycmFsJmNhbXBhaWduPShub3Qgc2V0KSZjb250ZW50PShub3Qgc2V0KSZleHBlcmltZW50PShub3Qgc2V0KSZ2YXJpYXRpb249KG5vdCBzZXQpJnVhPWVkZ2UmY2xpZW50X2lkX2dhND01MDEzNzE4NDguMTc0OTAwNDc0MyZzZXNzaW9uX2lkPTc3MjMwNTMyODQmZGxzb3VyY2U9bW96b3Jn&attribution_sig=7ba90acf45f025ea79b153fc3f23cd0c46d921bbcc0dbcf340eb123d007103ae&_gl=1*1w7f5lo*_ga*NTAxMzcxODQ4LjE3NDkwMDQ3NDM.*_ga_MQ7767QQQW*czE3NDkwMDQ3NDMkbzEkZzEkdDE3NDkwMDQ4NzYkajQ3JGwwJGgw",
                "old": r"https://ftp.mozilla.org/pub/firefox/releases/106.0b3/win64/en-US/Firefox%20Setup%20106.0b3.msi",
                "old_version": "106.0b3"
            },

            "CCleaner": {
                "extension": "msi",
                "latest": r"https://www.ccleaner.com/go/get_ccbe_msi",
                "old": r"old", #find later
                "old_version": "test3"
            },

            "Notepad++": {
                "extension": "msi",
                "latest": r"new",
                "old": r"old", #find later
                "old_version": "test6"
            }
        }
        
        for program in program_list.keys():
            if (program.lower() in p['name'].lower()):
                return Command(
                    #standerdized all placeholders to #---_replace# for easier replacement
                    #also added & REM which allows additional storeage in the command by adding a comment to it
                    #could've added another variable to command class but i thought this was cooler 👍
                    f"msiexec /i #{program}_replace# /qn & REM program_installed", 
                    prereq_required=True, 
                    supported_dict=program_list,
                    radio_button_options={
                        "questions": [
                            {
                                "question": f"What version of {program} did you want to install?",
                                "options": [
                                    f"Old Version ({program_list[program]['old_version']})", 
                                    "Latest Version"
                                ]
                            }
                        ]
                    }
                )
        
        return None
