class Translator:
    
    def __init__(self, config_dictionary):
        self.config_dictionary = config_dictionary
        self.commands_list = []
    
    def translate(self):
        for check in self.config_dictionary['check']:
            for check_pass in check['pass']:
                if check_pass['type'] == "FirewallUp":
                    # why not just interate though and call a method based on the type
                    # u gotta remember that this is going to an exe you can't just call it on the host machine
                    # so we'll have a base exe script that somehow we pass in params to like idk lets work
                    self.config_dictionary.append("") # you can just iterate through list and run everything