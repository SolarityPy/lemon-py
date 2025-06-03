import subprocess, os

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
    def user_in_group_command(p):
        pass
    # === COMMAND MAPPING ===
    commands = {
        # === USER COMMANDS ===
        #"feet": lambda p: f"feet{p}", (why is there a feet command :O - karl)
        "userexists": lambda p: f"net user {p['name']} /delete",
        "userexistsnot": lambda p: f"net user {p['name']} CyberPatriots1! /add",
        "userdetail": user_detail_command,
        "userdetailnot": user_detail_command,
        
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
