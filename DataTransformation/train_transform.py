"""
Author: Abhishek
Purpose: Data transformation code used in training part
"""
import os
import pandas as pd
from log_files import logs_list
from App_logging.logger import App_Logger

class TrainTranformation:
    def __init__(self) -> None:
        self.logs_list = logs_list()
        self.logger = App_Logger()

    def addQuotesToString(self, file_obj):
        """
        Description: Add quotes to all columns having string data type
        """
        try:
            good_files = [f for f in os.listdir(self.logs_list["good_raw"])]
            for file in good_files:
                data = pd.read_csv(os.path.join(self.logs_list["good_raw"], file))

                data["class"] = data["class"].apply(lambda x: "'"+str(x)+"'")
                data.to_csv(os.path.join(self.logs_list["good_raw"], file), index=None, header=None)

            self.logger.log(file_obj, "Quotes added successfully.")
        except Exception as e:
            self.logger.log(file_obj, "Data transformation failes: %s"%e)


