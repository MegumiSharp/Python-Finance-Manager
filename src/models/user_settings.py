import json
import os
from config.settings import (USER_SETTINGS_PATH, DEFAULT_USER_SETTINGS)        # Path to user settings JSON file and default settings

# UserSettings class to handle user settings stored in a JSON file It provides methods to read and change settings in the user_settings.json file
class UserSettings:
    def __init__(self):
        self.__create_user_settings_json()  # Ensure the JSON file exists
    
    def read_json_value(self, key: str):
        with open(USER_SETTINGS_PATH, "r") as f:
            data = json.load(f)
        return str(data[key])
    
    def change_json_value(self, key: str, value:str):
        with open(USER_SETTINGS_PATH, "r") as f:
            data = json.load(f)

        #Update the value for the specified key
        if key not in data:
            raise KeyError(f"Key '{key}' not found in user settings.")
        if value is None:
            raise ValueError(f"Value for key '{key}' cannot be None.")
        if not isinstance(value, str):
            raise TypeError(f"Value for key '{key}' must be a string.")
        if value == "":
            raise ValueError(f"Value for key '{key}' cannot be an empty string.")
        data[key] = value

        with open(USER_SETTINGS_PATH, "w") as f:
            json.dump(data, f, indent=4)

    # Private method to check if the user_settings.json file exists
    def __does_file_exist(self):
        try:
            with open(USER_SETTINGS_PATH, "r") as f:
                return True
        except FileNotFoundError:
            return False
        
    # Private method to create the user_settings.json file with default settings if it doesn't exist
    def __create_user_settings_json(self):
        if not self.__does_file_exist() or os.path.getsize(USER_SETTINGS_PATH) == 0:
            with open(USER_SETTINGS_PATH, "w") as f:
                json.dump(DEFAULT_USER_SETTINGS, f, indent=4)