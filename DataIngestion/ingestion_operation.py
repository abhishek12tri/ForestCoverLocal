"""
Author: Abhishek
Purpose: Handles data ingestion operationfor training and predition
"""
import os
import pandas as pd
from App_logging.logger import App_Logger
from log_files import logs_list

class Ingestion:
    def __init__(self) -> None:
        self.log_list = logs_list()
        self.logger = App_Logger()

    def get_training_data(self, file_obj):
        """Description: Reads the data from source."""
        try:
            data = pd.read_csv(os.path.join(self.log_list["file_from_DB"], self.log_list["inputfile"]))
            self.logger.log(file_obj, "Data loaded successfully.")
            return data

        except Exception as e:
            self.logger.log(file_obj, "Error in data loading: %s"%e)
            raise e