"""
Author: Abhishek
Purpose: Validate prediction data
"""
import os
import re
import json
import shutil
import pandas as pd
from App_logging.logger import App_Logger
from log_files import logs_list


class RawValidate:
    def __init__(self, path) -> None:
        self.path_dir = path
        self.schema_path = "schema_prediction.json"
        self.logger = App_Logger()
        self.log_list = logs_list()

    def valuesFromSchema(self, file_obj):
        """
        Description: Extract all relevant info from pre-defined Schema
        """
        try:
            with open(self.schema_path, "r") as f:
                dic = json.load(f)
            LenOfDate = dic["LengthOfDateStampInFile"]
            LenOfTime = dic["LengthOfTimeStampInFile"]
            column_name = dic["ColName"]
            NumColumns = dic["NumberofColumns"]

            self.logger.log(file_obj, "Read Schema data.")
            return LenOfDate, LenOfTime, column_name, NumColumns

        except Exception as e:
            self.logger.log(file_obj, "Error in reading schema data: "+ str(e))
            raise e

    def manual_regex_creation(self):
        """
        Description: Regex code to validate filename
        """
        return "['forest_cover']+['\_'']+[\d_]+[\d]+\.csv"
    
    def validate_file(self, regex, DateSample, TimeSample, file_obj):
        """
        Description: Validate filename
        """
        files = [f for f in os.listdir(self.path_dir)]
        try:
            for filename in files:
                if re.match(regex, filename):
                    name_split = re.split(".csv", filename)
                    split_file = re.split('_', name_split[0])

                    if len(split_file[2]) == DateSample:
                        if len(split_file[3]) == TimeSample:
                            self.logger.log(file_obj, "Filename satisfied: "+str(filename))
                        else:
                            shutil.move(self.path_dir+filename, self.log_list["pred_error_files"])
                            self.logger.log(file_obj, "Filename Time not satisfied: "+str(filename)) 

                    else:
                        shutil.move(self.path_dir+filename, self.log_list["pred_error_files"])
                        self.logger.log(file_obj, "Filename Date not satisfied: "+str(filename))

                else:
                    shutil.move(self.path_dir+filename, self.log_list["pred_error_files"])
                    self.logger.log(file_obj, "Filename Regex not satisfied: "+str(filename))
        except Exception as e:
            self.logger.log("Error in validate_file: "+ str(e))
            raise e

    def validate_column_length(self, numColumns, file_obj):
        """
        Description: Validate column length
        """
        try:
            files = [f for f in os.listdir(self.path_dir)]
            for file in files:
                csv = pd.read_csv(self.path_dir+file)
                print(csv.shape, numColumns)
                if csv.shape[1] == numColumns:
                    csv.rename(columns={"Unnamed: 0": "Wafer"}, inplace=True)
                    csv.to_csv(self.path_dir+file, index=None, header=True)
                    self.logger.log(file_obj, "File column length satisfied: "+str(file))

                else:
                    shutil.move(self.path_dir+file, self.log_list["pred_error_files"])
                    self.logger.log(file_obj, "Filename column_length not satisfied: "+str(file))
        except Exception as e:
            self.logger.log(file_obj, "Error in column len validation: "+str(e))
            raise e

    def validateMissingValues(self, file_obj):
        """
        Description: To validate missing values in data.
        """
        try:
            files = [f for f in os.listdir(self.path_dir)]
            for file in files:
                csv = pd.read_csv(self.path_dir + file )
                count = 0
                for columns in csv:
                    if (len(csv[columns]) - csv[columns].count()) == len(csv[columns]):
                        count += 1
                        shutil.move(self.path_dir+file, self.log_list["pred_error_files"])
                        self.logger.log(file_obj, "Error in Missing values: "+str(file))
                        break

            self.logger.log(file_obj, "Validated missing values.")
        
        except Exception as e:
            self.logger.log(file_obj, "Error in missing values: "+str(e))
            raise e
        
    def load_data(self, file_obj):
        """
        Description: Load data from saved CSV file.
        """
        saved_file = os.path.join(self.path_dir, self.log_list["input_file"])
        try:
            data = pd.read_csv(saved_file)
            self.logger.log(file_obj, "Data Loaded.")

            return data
        except Exception as e:
            self.logger.log(file_obj, "Error in load data: ", str(e))