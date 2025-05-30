import json

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
                if check_type in self.types_dictionary:
                    #maybe a paramater list here
                    for parameter in self.types_dictionary[check_type]:
                        print(parameter)
                        #prob add to the list here
                    #then add to cmd_list by call to command creation method here?