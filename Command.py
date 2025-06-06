class Command:
    def __init__(self, command_string, prereq_required=False, open_ended_questions=None, radio_button_options=None):
        self.command_string = command_string
        self.prereq_questions_required = prereq_required # Boolean: True or False
        
        self.open_ended_questions = []

        
    def get_command(self):
        return self.command_string
    
    def get_prerequesite_commands(self):
        return self.prereq_commands