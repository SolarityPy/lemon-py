class Command:
    def __init__(self, command_string, prereq_required=False, open_ended_questions=None, radio_button_options=None):
        self.command_string = command_string
        self.prereq_questions_required = prereq_required # Boolean: True or False
        self.radio_button_options = radio_button_options
        self.open_ended_questions = open_ended_questions
        
        '''
        Radio Button Options Format
        {
            "questions": [
                {"question": "What version of __________ would you like to install?, "options": ["Old Version", "Latest"]}
            ]
        }

        
        
        
        '''

        
    def get_command(self):
        return self.command_string
    
    def get_prerequesite_commands(self):
        return self.prereq_commands
    
    def get_prereq_required(self):
        return self.prereq_questions_required