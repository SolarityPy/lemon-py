import json, os
if os.name == "nt":
    from WindowsCommands import Commands
else:
    from LinuxCommands import Commands
    
class Translator:
    def __init__(self, config_dictionary, root):
        self.config_dictionary = config_dictionary 
        self.commands_list = [] 
        self.root = root
        
        with open("check_types.json",  "r") as f:
            #dictionary that contains all Aeacus check types stored in a json file
            self.types_dictionary = json.load(f)

    def translate(self):
        for check in self.config_dictionary['check']:
            for check_pass in check['pass']:
                check_type = check_pass['type']
                
                commands_obj = Commands(self.root)
                command_method = commands_obj.commands.get(check_type.lower())
                
                if ("not" in check_pass['type'].lower()):
                    command_object = command_method(commands_obj, check_pass, True)
                else:
                    command_object = command_method(commands_obj, check_pass, False)
                    
                self.commands_list.append(command_object)
                
        return self.commands_list