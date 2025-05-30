class Translator:
    
    def __init__(self, config_dictionary):
        self.config_dictionary = config_dictionary 
        self.commands_list = [] #I was thinking and I was imagining that we just add the commands to list and then run them in the exe - might have been the original idea tho
    
    def translate(self):
        for check in self.config_dictionary['check']:
            for check_pass in check['pass']:
                if check_pass['type'] == "FirewallUp":
                    self.commands_list.append("")







#thought we might these real soon
'''
CommandContains:      ["cmd", "value"]
CommandOutput:        ["cmd", "value"]
DirContains:          ["path", "value"]
FileContains:         ["path", "value"]
FileEquals:           ["path", "value"]
FileOwner:            ["path", "name"]
FirewallUp:           []
PathExists:           ["path"]
ProgramInstalled:     ["name"]
ProgramVersion:       ["name", "value"]
ServiceUp:            ["name"]
UserExists:           ["name"]
UserInGroup:          ["user", "group"]
PasswordChanged:          ["user", "value"]
PermissionIs:             ["path", "value"]
AutoCheckUpdatesEnabled:  []
Command:                  ["cmd"]
GuestDisabledLDM:         []
KernelVersion:            ["value"]
PasswordChanged:          ["user", "after"]
PermissionIs:             ["path", "name", "value"]
BitlockerEnabled:         []
FirewallDefaultBehavior:  ["name", "value", "key"]
RegistryKeyExists:        ["key"]
ScheduledTaskExists:      ["name"]
SecurityPolicy:           ["key", "value"]
ServiceStartup:           ["name", "value"]
ShareExists:              ["name"]
UserDetail:               ["user", "key", "value"]
UserRights:               ["name", "value"]
WindowsFeature:           ["name"]
'''