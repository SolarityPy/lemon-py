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
                #standerdized all placeholders to #---_replace# for easier replacement
                #if you want more info on this go down like 20 lines
                f'net share {p['name']}="#share_replace#" & REM share_exists', 
                prereq_required=True, 
                open_ended_questions=["What path would you like the share to broadcast?"]
            )
        else:
            return Command(f"net share {p['name']} /delete") # delete the share
        

    def program_installed_command(self, p, not_boolean):
        program_list = {
            "Firefox": {
                "new_version": "Mozilla.Firefox",
                "old_version": "Mozilla.Firefox -v 96.0"
            },

            "CCleaner": {
                "new_version": "Piriform.CCleaner",
                "old_version": "Piriform.CCleaner"
            },

            "Notepad++": {
                "new_version": "Notepad++.Notepad++",
                "old_version": "Notepad++.Notepad++ -v 7.8.6" 
            },
            
            "Wireshark": {
                "new_version":"WiresharkFoundation.Wireshark",
                "old_version":"WiresharkFoundation.Wireshark -v 3.2.2"
            },

            "Google Chrome": {
                "new_version": "Google.Chrome",
                "old_version": "Google.Chrome"
            }

            
        }
        
        for program in program_list.keys():
            if (program.lower() in p['name'].lower()):
                return Command(
                    #standerdized all placeholders to #---_replace# for easier replacement
                    #also added & REM which allows additional storeage in the command by adding a comment to it
                    #could've added another variable to command class but i thought this was cooler 👍
                    #the reason for this change is that it allows us to dynamically change based on the name bc then we know what program they want and such
                    f"winget install --id #{program}_replace# -e --silent --accept-package-agreements --accept-source-agreements & REM program_installed", 
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

    def security_policy_command(self, p, not_boolean):
        pass

        
    