import subprocess, os
command_list = None

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
                print(f"✓ Success: {{command}}")
            else:
                print(f"✗ Failed: {{command}} - {{result.stderr}}")
                
        except Exception as e:
            print(f"✗ Error executing {{command}}: {{e}}")
            results.append({{
                'command': command,
                'error': str(e)
            }})
    return results

if __name__ == "__main__":
    print("\n\n Results:\n"+execute_all())
