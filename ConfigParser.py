import toml

class ConfigParser:
    # Note: no need for instance variables, using self auto creates
    # __init__ is constructor, also note that self is required for class methods
    
    def __init__(self, config_path):
        self.config_path = config_path
        
    # Let me know what you think, I want to parse it in a dictionary b/c it's easier to work with
    def parse(self):
        try:
            with open(self.config_path, 'r') as f:
                config = toml.load(f)
                return config
        except Exception as E:
            # Returns none and prints out error
            print(E)
            return None