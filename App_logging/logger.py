"""
Author: Abhishek
Purpose: Creates logs of the application
"""
from datetime import datetime

class App_Logger:
    def log(self, file_obj, message):
        self.now = datetime.now()
        date = self.now.date()
        crnt_time = self.now.strftime("%H:%M:%S")
        
        file_obj.write(
            str(date) + " " + str(crnt_time) + "\t\t" + message + "\n"
        )
