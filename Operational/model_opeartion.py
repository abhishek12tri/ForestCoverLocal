"""
Author: Abhishek
Purpose: Handles model operations like save and load model
"""
import pickle
import os
import shutil
from App_logging.logger import App_Logger
from log_files import logs_list

class FileOperation:
    def __init__(self) -> None:
        self.logger = App_Logger()
        self.files_list = logs_list()

    def save_model(self, model, filepath, file_obj):
        """Description: Saves the model."""
        try:
            # if os.path.isdir(self.files_list["model_dir"]):
            #     shutil.rmtree(self.files_list["model_dir"])
            if not os.path.isdir(self.files_list["model_dir"]):
                os.makedirs(self.files_list["model_dir"])

            with open(filepath+".sav", "wb") as f:
                pickle.dump(model, f)

            self.logger.log(file_obj, "Model file saved at "+filepath)


        except Exception as e:
            self.logger.log(file_obj, "Error in saving ", e)
            raise e


