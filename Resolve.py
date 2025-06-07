from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage, CTkRadioButton
import tkinter as tk
class Resolve:
    def __init__(self, root, command_obj_list, hub_callback=None, user_answers=None):
        self.root = root
        self.command_obj_list = command_obj_list
        self.hub_callback = hub_callback

        self.index = 1
        self.question_formatted_list = []
        if user_answers:
            self.user_answers = user_answers
        else:
            self.user_answers = {}
        self.radio_var = tk.StringVar()  # Make it persistent

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def update_screen(self):
        self.clear_screen()
        question_dict = self.question_formatted_list[self.index - 1]
        
        # Configure grid once
        for i in range(3):
            self.root.grid_columnconfigure(i, weight=1)
        for i in range(5):
            self.root.grid_rowconfigure(i, weight=1)
        
        # Center the question label
        label = CTkLabel(self.root, text=question_dict['question'])
        label.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")
        
        if question_dict['type'] == "radio_options":
            # Restore previous answer if exists
            if self.index in self.user_answers:
                self.radio_var.set(self.user_answers[self.index])
            else:
                self.radio_var.set("")
            
            # Center the radio buttons
            for i, option in enumerate(question_dict['options']):
                radio_btn = CTkRadioButton(
                    self.root,
                    text=option,
                    variable=self.radio_var,
                    value=option
                )
                radio_btn.grid(row=i+1, column=1, pady=5, padx=20, sticky="nswe")
        
        # Create buttons
        back_button = CTkButton(self.root, text="Back", height=30, width=120, command=self.decrease_index)
        escape_button = CTkButton(self.root, text="Escape", height=30, width=120, command=self.resolve_escape)
        next_button = CTkButton(self.root, text="Next", height=30, width=120, command=self.increase_index)
        
        # Show appropriate buttons
        if self.index > 1:
            back_button.grid(row=4, column=0, padx=20, pady=10, sticky="ws")
        else:
            escape_button.grid(row=4, column=0, padx=20, pady=10, sticky="ws")

        if  self.index < len(self.question_formatted_list):
            next_button.grid(row=4, column=2, padx=(20,0), pady=10, sticky="se")
        else:
            escape_button.grid(row=4, column=2, padx=(20,0), pady=10, sticky="se")

    def init(self): 
        self.root.geometry("600x450")
        self.clear_screen()
        
    def increase_index(self):
        self.save_current_answer()
        if self.index < len(self.question_formatted_list): 
            self.index += 1
            self.update_screen()
        
    def decrease_index(self):
        self.save_current_answer()
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

    def resolve_escape(self):
        self.save_current_answer()
        self.update_commands_with_answers()
        self.hub_callback(self.user_answers)
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

    def save_current_answer(self):
        #Save current selection before navigating
        current_answer = self.radio_var.get()
        if current_answer:
            self.user_answers[self.index] = current_answer
            # Update commands immediately when answer changes
            self.update_commands_with_answers()

    def update_commands_with_answers(self):
        """Update command strings based on current user answers"""
        question_index = 1
        for command_obj in self.command_obj_list:
            if command_obj.get_prereq_required():
                if command_obj.radio_button_options:
                    for radio_option in command_obj.radio_button_options['questions']:
                        if question_index in self.user_answers:
                            answer = self.user_answers[question_index]
                            # Update the command string based on the answer
                            command_obj.update_command_with_answer(question_index, answer)
                        question_index += 1
        
        # Print updated commands after each answer
        print("=== UPDATED COMMANDS ===")
        for i, command_obj in enumerate(self.command_obj_list):
            print(f"Command {i+1}: {command_obj.get_command()}")
        print()