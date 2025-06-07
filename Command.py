class Command:
    # Class-level replacement mappings
    PLACEHOLDER_HANDLERS = {
        "#file_msi_path#": "_get_msi_path",
        "#share_path#": "_get_direct_replacement", 
        "#program_version#": "_get_program_version"
    }
    
    def __init__(self, command_string, prereq_required=False, supported_command_dict=None, open_ended_questions=None, radio_button_options=None):
        self.command_string = command_string
        self.prereq_questions_required = prereq_required # Boolean: True or False
        self.supported_command_dict = supported_command_dict
        self.radio_button_options = radio_button_options
        self.open_ended_questions = open_ended_questions
        
    def get_command(self):
        return self.command_string
    
    def get_prerequesite_commands(self):
        return self.prereq_commands
    
    def get_prereq_required(self):
        return self.prereq_questions_required
    
    def update_command_with_answer(self, question_index, answer):
        for placeholder, handler_name in self.PLACEHOLDER_HANDLERS.items():
            if placeholder in self.command_string:
                handler = getattr(self, handler_name)
                replacement = handler(answer)
                if replacement is not None:
                    self.command_string = self.command_string.replace(placeholder, replacement)
    
    def _get_direct_replacement(self, answer):
        """For simple direct replacements"""
        return answer