from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage, CTkRadioButton
import tkinter as tk
from gui.title import Title
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
        self.current_entry = None

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
            
    def update_screen(self):
        self.clear_screen()

        # Configure the root grid properly
        self.root.rowconfigure(0, weight=0)  # Title bar
        self.root.rowconfigure(1, weight=1)  # Content pane
        self.root.rowconfigure(2, weight=0)
        
        for i in range(4):
            self.root.columnconfigure(i, weight=1)

        title = Title(self.root)
        title.title_bar_setup()
        
        # Content pane should expand to fill available space
        self.content_pane = CTkFrame(self.root, corner_radius=0, height=800, fg_color="#2B2929")
        self.content_pane.grid(row=1, column=0, rowspan=5, columnspan=4, sticky="nsew")

        # Configure content_pane internal grid
        for i in range(5):
            self.content_pane.rowconfigure(i, weight=1)
        for i in range(4):
            self.content_pane.columnconfigure(i, weight=1)
        
        try:
            question_dict = self.question_formatted_list[self.index - 1]
            
            if question_dict['type'] == "radio_options":
                label = CTkLabel(self.content_pane, text=question_dict['question'])
                label.grid(row=0, column=0, columnspan=3, pady=20, sticky="n")
                # Restore previous answer if exists
                if self.index in self.user_answers:
                    self.radio_var.set(self.user_answers[self.index])
                else:
                    self.radio_var.set("")
                
                for i, option in enumerate(question_dict['options']):
                    radio_btn = CTkRadioButton(
                        self.content_pane,
                        text=option,
                        variable=self.radio_var,
                        value=option
                    )
                    radio_btn.grid(row=i+1, column=1, pady=5, padx=20, sticky="nswe")
            elif question_dict['type'] == "open_ended":
                for question in question_dict['questions']:
                    label = CTkLabel(self.content_pane, text=question)
                    label.grid(row=0, column=0, columnspan=3, pady=20, sticky="new")
                    
                    self.current_entry = CTkEntry(self.content_pane, width=300, height=30)
                    self.current_entry.grid(row=1, column=1, pady=10, padx=20, sticky="ew")

                    #saves answer for later resoration
                    if self.index in self.user_answers:
                        self.current_entry.insert(0, self.user_answers[self.index])
        except:
            #accounts for case where user has nothing to resolve i.e. no user input needed
            nothing_label = CTkLabel(self.content_pane, text="*You have nothing to resolve*", font=("Arial", 25, "bold"))
            nothing_label.place(relx=0.5, rely=0.45, anchor="center")

        # Create buttons
        back_button = CTkButton(self.content_pane, text="Back", height=30, width=120, command=self.decrease_index)
        escape_button = CTkButton(self.content_pane, text="Escape", height=30, width=120, command=self.resolve_escape)
        next_button = CTkButton(self.content_pane, text="Next", height=30, width=120, command=self.increase_index)
        
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
        root = self.root
        root.geometry("650x450")
        self.clear_screen()
        
        for i in range(4):
            root.rowconfigure(i, weight=1)

        for i in range(4): 
            root.columnconfigure(i, weight=1)

        
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

        for i in range(3):
            root.grid_columnconfigure(i, weight=1)
        for i in range(5):
            root.grid_rowconfigure(i, weight=1)

        self.update_screen()

    def resolve_escape(self):
        try:
            #same thing handles case where no user input needed so obiously it cant save a answer
            self.save_current_answer()
            self.update_commands_with_answers()
        finally:
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
        #save current selection before navigating
        question_dict = self.question_formatted_list[self.index - 1]
        #saves radio options
        if question_dict['type'] == "radio_options":
            current_answer = self.radio_var.get()
            if current_answer:
                self.user_answers[self.index] = current_answer
        #saves open ended questions
        elif question_dict['type'] == "open_ended":
            if self.current_entry:
                    current_answer = self.current_entry.get()
                    if current_answer:
                        self.user_answers[self.index] = current_answer
        # update commands when answer changes
        self.update_commands_with_answers()

    def update_commands_with_answers(self):
        """Update command strings based on current user answers"""
        question_index = 1 #starts at one to match indexing of user_answers {1: "answer" , 2: "answer2", ect.}
        for command_obj in self.command_obj_list:
            if command_obj.get_prereq_required():
                if command_obj.radio_button_options:
                    for radio_option in command_obj.radio_button_options['questions']:
                        if question_index in self.user_answers:
                            answer = self.user_answers[question_index] 
                            #calls update command in command class with radio button
                            command_obj.update_command_with_answer(answer)
                        question_index += 1

                elif command_obj.open_ended_questions:
                    for question in command_obj.open_ended_questions:
                        if question_index in self.user_answers:
                            answer = self.user_answers[question_index]
                            #calls update in command class with open ended
                            command_obj.update_command_with_answer(answer)
                        question_index += 1
        
        #print updated commands after each answer so we like know what were doing
        print("=== UPDATED COMMANDS AFTER USER INPUT ===")
        for i, command_obj in enumerate(self.command_obj_list):
            print(f"Command {i+1}: {command_obj.get_command()}")
        print()