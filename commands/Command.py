class Command:
    placeholder_handlers = {
        #add placeholders that dont need a supported_dict
        "#share_replace#": "get_answer"
    }
    
    def __init__(self, command_string, prereq_required=False, supported_dict=None, open_ended_questions=None, radio_button_options=None):
        self.original_command = command_string
        self.command_string = command_string
        self.prereq_questions_required = prereq_required # Boolean: True or False
        self.supported_dict = supported_dict
        self.radio_button_options = radio_button_options
        self.open_ended_questions = open_ended_questions
        
    def get_command(self):
        return self.command_string
    
    def set_command(self, command_string):
        self.command_string = command_string
    
    def get_prerequesite_commands(self):
        return self.prereq_commands
    
    def get_prereq_required(self):
        return self.prereq_questions_required
    
    def update_command_with_answer(self, answer):
        self.reset_command()
        # installed command handleing will need something similer for all other ones that need a dictionary
        # other than that can use the placeholder_handler
        # TLDR: first part is for handling of dictionaries of dictionaries and second is for handling non-dictionary (supported_dict=None) placeholders
        if self.supported_dict:
            for dict_key in self.supported_dict.keys():
                dict_placeholder = f"#{dict_key}_replace#"
                if dict_placeholder in self.command_string:
                    replacement = self.get_replacement(dict_key, answer)
                    if replacement:
                        self.command_string = self.command_string.replace(dict_placeholder, replacement)
        
        # handle standard placeholders
        for placeholder, handler_name in self.placeholder_handlers.items():
            if placeholder in self.command_string:
                #returns method - allows different standard placeholders to call different methods
                handler = getattr(self, handler_name, None)
                if handler:
                    replacement = handler(answer)
                    if replacement is not None:
                        self.command_string = self.command_string.replace(placeholder, replacement)
    
    def get_replacement(self, key, answer):
        #add more if staments for other dictionary requiring commands
        if ('program_installed' in self.command_string):
            return self.get_program_msi(key, answer)

    def get_program_msi(self, key, answer):
        #specifically for program installed will only be used for that
        if key in self.supported_dict:
            program = self.supported_dict[key]
            if 'Old Version' in answer:
                return program['old_version']
            else:
                return program['new_version']
        return None

    def get_answer(self, answer):
        #allows dictionaried placeholders to acsess their answer
        return answer
    
    def reset_command(self):
        #called when changing a answer in resolve because it needs the placeholder to replace with new value
        self.command_string = self.original_command