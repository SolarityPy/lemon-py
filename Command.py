class Command:
    def __init__(self, command, prequesite_commands = None):
        self.command = command
        self.prequesite_commands = prequesite_commands