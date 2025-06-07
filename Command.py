class Command:
    PLACEHOLDER_HANDLERS = {
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
        # Handle dynamic program placeholders (e.g., #Firefox_msi_path#)
        if self.supported_command_dict:
            for program_name in self.supported_command_dict.keys():
                program_placeholder = f"#{program_name}_msi_path#"
                if program_placeholder in self.command_string:
                    replacement = self._get_program_msi_path(program_name, answer)
                    if replacement:
                        self.command_string = self.command_string.replace(program_placeholder, replacement)
        
        # Handle standard placeholders
        for placeholder, handler_name in self.PLACEHOLDER_HANDLERS.items():
            if placeholder in self.command_string:
                handler = getattr(self, handler_name, None)
                if handler:
                    replacement = handler(answer)
                    if replacement is not None:
                        self.command_string = self.command_string.replace(placeholder, replacement)
    
    def _get_direct_replacement(self, answer):
        """For simple direct replacements"""
        return answer

    def _get_program_version(self, answer):
        """Extract version from answer"""
        if "Old Version" in answer:
            import re
            match = re.search(r'\((.*?)\)', answer)
            return match.group(1) if match else "old"
        elif "Latest Version" in answer:
            return "latest"
        return None
    
    def _get_program_msi_path(self, program_name, answer):
        """Get the correct MSI path based on program and user answer"""
        if not self.supported_command_dict or program_name not in self.supported_command_dict:
            return None
            
        program_data = self.supported_command_dict[program_name]
        
        if "Old Version" in answer:
            return program_data.get('old', '')
        elif "Latest Version" in answer:
            return program_data.get('latest', '')
        
        return None