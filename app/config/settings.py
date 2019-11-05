import os
from configparser import ConfigParser


class Settings:
    def __init__(self, **kwargs):
        current_dir = os.getcwd()
        config_path = os.path.join(current_dir, 'config')
        config = ConfigParser()    
        config.read('C:\\Users\\Zadigo\\Documents\\Apps\\startup_nation\\app\\config\\settings.ini')
        config.set('DEFAULT', 'path', current_dir)
        config.set('DEFAULT', 'config', current_dir+'a')

        with open('C:\\Users\\Zadigo\\Documents\\Apps\\startup_nation\\app\\config\\settings.ini', 'w') as f:
            config.write(f)

    def check_file(self):
        pass

    def writer(self):
        pass
    
    @property
    def get_questions_raw_file(self):
        return None

settings = Settings()
