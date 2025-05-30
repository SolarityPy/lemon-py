import json
from Security import Security

class Translator:
    def __init__(self, config_dictionary):
        self.config_dictionary = config_dictionary 
        self.commands_list = []
        with open("check_types.json",  "r") as f:
            #dictionary that contains all Aeacus check types stored in a json file
            self.types_dictionary = json.load(f)
    
    def translate(self):
        for check in self.config_dictionary['check']:
            for check_pass in check['pass']:
                check_type = check_pass['type']
                output = getattr(Security, check_type.lower())
                print(check_pass)
                self.commands_list.append(output(check_pass)) # output takes in dict
        print(self.commands_list)