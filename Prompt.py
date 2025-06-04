from tkinter import filedialog 
class Prompt:
    @staticmethod
    def prompt():
        file = filedialog.askopenfile()
        return file