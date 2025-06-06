from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage

class Resolve:
    def __init__(self, root, command_obj_list):
        self.root = root
        self.command_obj_list = command_obj_list
        
        self.question_formatted_list = []

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def init(self): 
        self.root.geometry("300x450")
        self.clear_screen()

    def create_resolve(self):
        root = self.root
        self.init()
        
        index = 0
        back_button = CTkButton(root, text="Back", height = 30, padx = 10, pady = 10)
        next_button = CTkButton(root, text="Next", height = 30, padx = 10, pady = 10)
        
    def resolve(self):
        for command_obj in self.command_obj_list:
            if (command_obj.get_prereq_required()):
                if (command_obj.open_ended_questions != None and len(command_obj.open_ended_questions) != 0):
                    self.question_formatted_list.append({
                        "type": "open_ended", 
                        "questions": command_obj.open_ended_questions,
                        "answer": ["" for x in command_obj.open_ended_questions]
                    })
                elif (command_obj.radio_button_options != None and len(command_obj.radio_button_options) != 0):
                    for radio_option in command_obj.radio_button_options['questions']:
                        self.question_formatted_list.append({
                            "type": "radio_options",
                            "question": radio_option['question'],
                            "options": radio_option['options']
                        })
                        
        print(self.question_formatted_list)