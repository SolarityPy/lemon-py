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
    def download(path, url):
        r = requests.get(url)
        if r.status_code == 200:
            with open(path, 'wb') as file:
                file.write(r.content)
                return True
        else:
            return None    
        
    @staticmethod
    def program_installed_command(p, not_boolean): # In the future, Lemon will ask the user for any required programs: Lemon will use this check as penalty
        program_list = {
            "firefox": {
                "extension": "msi",
                "latest": "https://download.mozilla.org/?product=firefox-msi-latest-ssl&os=win64&lang=en-US&attribution_code=c291cmNlPXN1cHBvcnQubW96aWxsYS5vcmcmbWVkaXVtPXJlZmVycmFsJmNhbXBhaWduPShub3Qgc2V0KSZjb250ZW50PShub3Qgc2V0KSZleHBlcmltZW50PShub3Qgc2V0KSZ2YXJpYXRpb249KG5vdCBzZXQpJnVhPWVkZ2UmY2xpZW50X2lkX2dhND01MDEzNzE4NDguMTc0OTAwNDc0MyZzZXNzaW9uX2lkPTc3MjMwNTMyODQmZGxzb3VyY2U9bW96b3Jn&attribution_sig=7ba90acf45f025ea79b153fc3f23cd0c46d921bbcc0dbcf340eb123d007103ae&_gl=1*1w7f5lo*_ga*NTAxMzcxODQ4LjE3NDkwMDQ3NDM.*_ga_MQ7767QQQW*czE3NDkwMDQ3NDMkbzEkZzEkdDE3NDkwMDQ4NzYkajQ3JGwwJGgw",
                "old": r"https://ftp.mozilla.org/pub/firefox/releases/106.0b3/win64/en-US/Firefox%20Setup%20106.0b3.msi",
                "old_version": "106.0b3"

                
            }
        }
        # we're going to need some prompt function, it pops up the box and asks the user whether they want the latest or out of date
        choice = input(f"Latest version of {p['name']}? (y/n: installs old)")
        
        if choice.lower() == "y": old_version = False 
        else: old_version = True
        
        for program in program_list.keys():
            if p['name'].lower() in program or program in p['name'].lower:
                download_url = program_list[program]["latest" if not old_version else "old"]
                extension = program_list[program]['extension']
                
                file_name = f"{program}.{extension}"
                if Commands.download(file_name, download_url):
                    if extension == "msi":
                        return file_name + " /qn"
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
        
        "userrights": lambda p: f"ntrights -r {p['value']} -u {p['name']}",
        "userrightsnot": lambda p: f"ntrights +r {p['value']} -u {p['name']}",
        
        # === SECURITY COMMANDS ===
        "firewallup": lambda p: "netsh advfirewall set allprofiles state off",
        "firewallupnot": lambda p: "netsh advfirewall set allprofiles state on",
        
        # === WINDOWS FEATURES ===
        "windowsfeature": lambda p: f"Dism /Online /Disable-Feature /FeatureName:{p['name']}",
        "windowsfeaturenot": lambda p: f"Dism /Online /Enable-Feature /FeatureName:{p['name']}",
        
        # === SERVICES ===
        "serviceup": lambda p: f"sc stop '{p['name']}'",
        "serviceupnot": lambda p: f"sc start '{p['name']}'",

        "servicestartup": lambda p: f"sc config '{p['name']}' start='{"disabled" if p['startup'] == 'automatic' else 'auto'}'",
        "servicestartupnot": lambda p: f"sc config '{p['name']}' start='{"auto" if p['startup'] == 'automatic' else 'disabled'}'",
        

        
        "programinstalled": program_installed_command,
        "programinstallednot": program_installed_command,

        # === MISCELLANEOUS ===
        "shareexists": lambda p: f"net share '{p['name']}' /delete",
        "shareexistsnot": lambda p: f"net share '{p['name']}'="
        
    }
