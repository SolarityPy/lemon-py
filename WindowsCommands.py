import subprocess, os, requests

class Commands:
    
    # === COMPLEX COMMAND FUNCTIONS ===
    @staticmethod
    def user_detail_command(p, not_boolean):
        if p['key'].lower() == "fullname" :
            return f"net user '{p['user']}' /fullname:\"\""
        
        elif p['key'].lower() == "isenabled":
            # not not_boolean is our normal condition that we coded first, assuming it's not a Not type
            if not not_boolean:
                if p['value'].lower() == "yes":
                    return f"net user '{p['user']}' /active:no"
                else:
                    return f"net user '{p['user']}' /active:yes"
            else: # Not type (ex. UserDetailNot), i just reversed them
                if p['value'].lower() == "yes":
                    return f"net user '{p['user']}' /active:yes"
                else:
                    return f"net user '{p['user']}' /active:no"
            
        elif p['key'].lower() == "isadmin":
            if not not_boolean:
                if p['value'].lower() == "yes":
                    return f"net localgroup Administrators '{p['user']}' /delete"
                else:
                    return f"net localgroup Administrators '{p['user']}' /add"
            else:
                if p['value'].lower() == "yes":
                    return f"net localgroup Administrators '{p['user']}' /add"
                else:
                    return f"net localgroup Administrators '{p['user']}' /delete"
        
        elif p['key'].lower() == "passwordneverexpires":
            if not not_boolean:
                if p['value'].lower() == "yes":
                    return f"WMIC USERACCOUNT WHERE Name='{p['user']}' SET PasswordExpires=FALSE"
                else:
                    return f"WMIC USERACCOUNT WHERE Name='{p['user']}' SET PasswordExpires=TRUE"
            else:
                if p['value'].lower() == "yes":
                    return f"WMIC USERACCOUNT WHERE Name='{p['user']}' SET PasswordExpires=TRUE" 
                else:
                    return f"WMIC USERACCOUNT WHERE Name='{p['user']}' SET PasswordExpires=FALSE"
                
        elif p['key'].lower() == "nopasswordchange":
            if not not_boolean:
                if p['value'].lower() == "yes":
                    return f"net user '{p['user']}' /PasswordChg:No"
                else:
                    return f"net user '{p['user']}' /PasswordChg:Yes"
            else:
                if p['value'].lower() == "yes":
                    return f"net user '{p['user']}' /PasswordChg:Yes"
                else:
                    return f"net user '{p['user']}' /PasswordChg:No"
            
    @staticmethod
    def program_installed_command(p, not_boolean): # In the future, Lemon will ask the user for any required programs: Lemon will use this check as penalty
        program_list = {
            "firefox": {
                "extension": "exe",
                "latest": "https://download.mozilla.org/?product=firefox-stub&os=win&lang=en-US",
                "old": "http://software.oldversion.com/download.php?f=YTo1OntzOjQ6InRpbWUiO2k6MTc0ODk3MzQwNztzOjI6ImlkIjtpOjQxMjAzO3M6NDoiZmlsZSI7czoyODoibW96aWxsYS1maXJlZm94LTQ2LTAtMS0wLmV4ZSI7czozOiJ1cmwiO3M6NTg6Imh0dHA6Ly93d3cub2xkdmVyc2lvbi5jb20vd2luZG93cy9tb3ppbGxhLWZpcmVmb3gtNDYtMC0xLTAiO3M6NDoicGFzcyI7czozMjoiZWU0NmQzMzBjYTA5ZTJmMjYzY2FhMzc4ZTEwYzU1OWQiO30%3D",
            }
        }
        # we're going to need some prompt function, it pops up the box and asks the user whether they want the latest or out of date
        old_version = False
        
        for program in program_list.keys():
            if p['name'].lower() in program or program in p['name'].lower:
                download_url = program_list[program]["latest" if not old_version else "old"]
                extension = program_list[program]['extension']
                with open(f"./{program}.{extension}"):
                    pass
                    
        pass

    commands = {
        # === USER COMMANDS ===
        # Note: https://www.tenforums.com/attachments/tutorial-test/142289d1499096195-change-user-rights-assignment-security-policy-settings-windows-10-a-ntrights.zip
        # Only way to change user rights assignment is to use this program, first dependency :(
            
        "userexists": lambda p: f"net user {p['name']} /delete",
        "userexistsnot": lambda p: f"net user {p['name']} CyberPatriots1! /add",
        
        "userdetail": user_detail_command,
        "userdetailnot": user_detail_command,
        
        "useringroup": lambda p: f"net localgroup '{p['group']}' '{p['user']}' /delete",
        "useringroupnot": lambda p: f"net localgroup '{p['group']}' '{p['user']}' /add",
        
        # === SECURITY COMMANDS ===
        "firewallup": lambda p: "netsh advfirewall set allprofiles state off",
        "firewallupnot": lambda p: "netsh advfirewall set allprofiles state on",
        
        # === WINDOWS FEATURES ===
        "windowsfeature": lambda p: f"Dism /Online /Disable-Feature /FeatureName:{p['name']}",
        "windowsfeaturenot": lambda p: f"Dism /Online /Enable-Feature /FeatureName:{p['name']}",
        
        # === SERVICES ===
        "serviceup": lambda p: f"sc stop {p['name']}",
        "serviceupnot": lambda p: f"sc start {p['name']}",
    }
