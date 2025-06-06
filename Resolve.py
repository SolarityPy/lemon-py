from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage, CTkRadioButton
import tkinter as tk
class Resolve:
    def __init__(self, root, command_obj_list):
        self.root = root
        self.command_obj_list = command_obj_list
        self.index = 1
        self.question_formatted_list = []

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def update_screen(self):
        self.clear_screen()
        question_dict = self.question_formatted_list[self.index - 1]
        
        # Center the question label
        label = CTkLabel(self.root, text=question_dict['question'])
        label.grid(row=0, column=0, columnspan=3, pady=20)
        
        if question_dict['type'] == "radio_options":
            self.radio_var = tk.StringVar(value="")
            
            # Center the radio buttons
            for i, option in enumerate(question_dict['options']):
                radio_btn = CTkRadioButton(
                    self.root,
                    text=option,
                    variable=self.radio_var,
                    value=option
                )
                # Place radio buttons in center column with some padding
                radio_btn.grid(row=i+1, column=1, pady=5, padx=20, sticky="w")
        
        # Recreate the Back and Next buttons
        back_button = CTkButton(self.root, text="Back", height=30, width=120, command=self.decrease_index)
        next_button = CTkButton(self.root, text="Next", height=30, width=120, command=self.increase_index)
        back_button.grid(row=4, column=0, padx=20, pady=10)
        next_button.grid(row=4, column=2, padx=20, pady=10)

    def init(self): 
        self.root.geometry("600x450")
        self.clear_screen()
        
    def increase_index(self):
        if self.index < len(self.question_formatted_list): 
            self.index += 1
            self.update_screen()
        
    def decrease_index(self):
        if self.index > 1: 
            self.index -= 1
            self.update_screen()

    def create_resolve(self):
        root = self.root
        self.init()

        # Configure grid for centering - 3 columns
        for i in range(3):
            root.grid_columnconfigure(i, weight=1)
        for i in range(5):  # Increased rows for radio buttons
            root.grid_rowconfigure(i, weight=1)

        self.update_screen()  # This will now create everything including buttons
        
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
                        
        self.create_resolve()