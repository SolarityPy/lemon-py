import subprocess, os

class Build:
    def __init__(self, command_object_list, hub_callback):
        self.command_object_list = command_object_list
        self.hub_callback = hub_callback
        
    def build_exe(self):
        commands_list = [x.get_command() for x in self.command_object_list]
        commands_repr = repr(commands_list)
        command_runner_script = f'''import subprocess, os
command_list = {commands_repr}

def execute_all():
    results = []
    for command in command_list:
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            results.append({{
                'command': command,
                'returncode': result.returncode,
                'stdout': result.stdout,
                'stderr': result.stderr
            }})
            
            if result.returncode == 0:
                print(f"Success: {{command}}")
            else:
                print(f"Failed: {{command}} - {{result.stderr}}")
                
        except Exception as e:
            print(f"Error executing {{command}}: {{e}}")
            results.append({{
                'command': command,
                'error': str(e)
            }})
    return results

if __name__ == "__main__":
    execute_all()'''
    
        script_path = os.path.join(os.getcwd(), "DynamicCommandExecutor.py")
        with open(script_path, "w") as fp:
            fp.write(command_runner_script)
        print(script_path)
        subprocess.run(f'pyinstaller --onefile --name "Run_Me" "{script_path}"')
        print("Created exe!")
    
    def build_linux():
        pass