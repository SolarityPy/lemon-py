from customtkinter import CTk, CTkLabel, CTkButton, CTkEntry, CTkFrame, CTkScrollableFrame, CTkImage

class EditCommands:
    def __init__(self, root, command_object_list, hub_callback):
        self.root = root
        self.command_object_list = command_object_list
        self.hub_callback = hub_callback

    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        
    def init(self):
        self.root.geometry("650x450")
        self.clear_screen()
        self.scroll_frame = CTkScrollableFrame(self.root, width=650, height=450)
        self.scroll_frame.grid(row=0, column=0, sticky="nsew")

    def create_EditCommands(self):
        self.init()

        self.scroll_frame.columnconfigure(0, weight=1)
        self.scroll_frame.columnconfigure(1, weight=1)

        info_text = CTkLabel(self.scroll_frame, text=f"*Commands with #placeholders# will be resolved during the resolve step*", font=("Arial", 16, "bold"))
        info_text.grid(row=0, column=0, columnspan=2, padx=10, pady=5, sticky="we")
        
        i = 1
        for command in self.command_object_list:
            self.scroll_frame.rowconfigure(i, weight=1)
            self.scroll_frame.rowconfigure(i+1, weight=1)

            #this avoids a bug where it cuts of the last letter of a normal command with no user input bc find returns -1 and it does [0:-1]
            if command.get_command().find("&") != -1:
                command_string = command.get_command()[0:command.get_command().find("&")]
            else:
                command_string = command.get_command()

            command_text = CTkLabel(self.scroll_frame, text=f"Command: {command_string}", font=("Arial", 16))
            command_text.grid(row=i, column=0, columnspan=2, padx=10, pady=5, sticky="we")

            edit_btn = CTkButton(self.scroll_frame, text="Edit", command=lambda: self.edit_command(), height=30, width=50, font=("Arial", 16, "bold"))
            edit_btn.grid(row=i+1, column=0, padx=10, pady=5, sticky="we")

            delete_btn = CTkButton(self.scroll_frame, text="Delete", command=lambda: self.delete_command(command.get_command()), height=30, width=50, font=("Arial", 16, "bold"))
            delete_btn.grid(row=i+1, column=1, padx=10, pady=5, sticky="we")
            
            i += 2
        #luckaly if you just don't put a row it will just put it at the next avaliable one so this one can always be at the bottom
        escape_btn = CTkButton(self.scroll_frame, text="Escape", command=self.escape_edit, height=30, width=70, font=("Arial", 16, "bold"))
        escape_btn.grid(column=0, columnspan=2, padx=10, pady=10, sticky="wes")


    def escape_edit(self):
        print("=== UPDATED COMMANDS AFTER EDITS ===")
        for i, command_obj in enumerate(self.command_object_list):
            print(f"Command {i+1}: {command_obj.get_command()}")
        print()
        self.hub_callback()

    def edit_command(self):
        pass

    def delete_command(self, del_command):
        for command in self.command_object_list:
            if command.get_command() == del_command:
                self.command_object_list.remove(command)
                break
        self.create_EditCommands()