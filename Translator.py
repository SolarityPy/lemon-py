import json, os
if os.name == "nt":
    from WindowsCommands import Commands
else:
    from LinuxCommands import Commands
    
class Translator:
    def __init__(self, config_dictionary):
        self.config_dictionary = config_dictionary 
        self.commands_list = [
            Command, Command, Command
        ] 
        self.pre_commmands_list = []
        
        with open("check_types.json",  "r") as f:
            #dictionary that contains all Aeacus check types stored in a json file
            self.types_dictionary = json.load(f)
    
    def translate(self):
        for check in self.config_dictionary['check']:
            for check_pass in check['pass']:
                check_type = check_pass['type']
                command_lambda = Commands.commands.get(check_type.lower())
                if ("not" in check_pass['type'].lower()):
                    command = command_lambda(check_pass, True)
                else:
                    command = command_lambda(check_pass, False)
                
                self.commands_list.append(command)
        print(self.commands_list)