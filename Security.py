import subprocess, os

"""
it's gonna be worse follow me to where i go


im telling you it will work better and be flexable
"""

class Security:
    @staticmethod
    def firewallup(param_dictionary): # needs same name as type, param dictionary can be empty but for sake of simplicity
        return "netsh advfirewall set allprofiles state off"
    
    @staticmethod
    def firewallupnot(param_dictionary):
        return "netsh advfirewall set allprofiles state on"
    
    @staticmethod
    def windowsfeature(param_dictionary): # checking if feature is installed
        return f"Dism /Online /Enable-Feature /FeatureName:{param_dictionary['name']}"
    
    @staticmethod
    def windowsfeaturenot(param_dictionary): # checking if feature is not installed
        return f"Dism /Online /Disable-Feature /FeatureName:{param_dictionary['name']}"
    
    @staticmethod
    def serviceup(param_dictionary):
        return f"sc stop {param_dictionary['name']}"
    
    @staticmethod
    def serviceupnot(param_dictionary):
        return f"sc start {param_dictionary['name']}"
        