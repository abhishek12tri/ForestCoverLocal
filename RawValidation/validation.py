"""
Author: Abhishek
Purpose: To handle raw data validation
"""
import os
import re
import json
import shutil
from log_files import logs_list
from App_logging.logger import App_Logger
import pandas as pd
from datetime import datetime


class DataValidation:
    def __init__(self, path) -> None:
        self.raw_dir = path
        self.schema_path = "schema_training.json"
        self.logs_list = logs_list()
        self.train_log_file = self.logs_list["train_log"]
        self.logger = App_Logger()

    def rawSchemaValues(self, file_obj):
        """
        Description: Gets data from pre-defined schema.
        """
        try:
            with open(self.schema_path, 'r') as f:
                schema_dict = json.load(f)

            LengthOfDate = schema_dict["LengthOfDateStampInFile"]
            LengthOfTime = schema_dict["LengthOfTimeStampInFile"]
            column_names = schema_dict["ColName"]
            NoOfColumn = schema_dict["NumberofColumns"]

            self.logger.log(file_obj, "Training Schema processed.")

            return LengthOfDate, LengthOfTime, column_names, NoOfColumn

            
        except Exception as e:
            self.logger.log(file_obj, str(e))
            raise ValueError

    def filename_checker(self):
        """
        Description: Regex filename for filename defined in schema.
        """
        regex = "['forest_cover']+['\_'']+[\d_]+[\d]+\.csv"
        return regex

    def validate_raw_files(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile, file_obj):
        """Description: This function validates the input file names CSV as per decided in schema."""

        self.deleteExistingBadDataFolder(file_obj)
        self.deleteExistingGoodDataFolder(file_obj)
        self.createGoodBadDataFolder(file_obj)
        
        self.logger.log(file_obj, "Good and bad data dir deletion and creation success.")

        onlyFiles = [f for f in os.listdir(self.raw_dir)]
        try:
            for filename in onlyFiles:
                if re.match(regex, filename):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = re.split('_', splitAtDot[0])
                    if len(splitAtDot[2]) == LengthOfDateStampInFile:
                        if len(splitAtDot[3]) == LengthOfTimeStampInFile:
                            shutil.copy(os.path.join(self.raw_dir, filename), self.logs_list["good_raw"])
                            
                        else:
                            shutil.copy(os.path.join(self.raw_dir, filename), self.logs_list["bad_raw"])
                            
                    else:
                        shutil.copy(os.path.join(self.raw_dir, filename), self.logs_list["bad_raw"])
                        
                else:
                    shutil.copy(os.path.join(self.raw_dir, filename), self.logs_list["bad_raw"])

            self.logger.log(file_obj, "Files moved to good and bad data dir.")     
        except Exception as e:

            self.logger.log(file_obj, 'Error occurred in validating (validate_raw_files): %s' % e)
            raise e

    def deleteExistingBadDataFolder(self, file_obj):
        """Description: To delete the existing Bad Data Folder."""
        try:
            if os.path.isdir(self.logs_list["bad_raw"]):
                shutil.rmtree(self.logs_list["bad_raw"])

        except OSError as e:
            self.logger.log(file_obj, 'Bad file deletion error: %s' % e)
            raise OSError

    def deleteExistingGoodDataFolder(self, file_obj):
        """Description: To delete the existing Good data Folder"""
        try:
            if os.path.isdir(self.logs_list["good_raw"]):
                shutil.rmtree(self.logs_list["good_raw"])
                
        except OSError as e:
            self.logger.log(file_obj, 'Good file deletion error: %s' % e)
            raise OSError

    def createGoodBadDataFolder(self, file_obj):
        """Description: To create data for Good data file: that will pass the CSV file name with Regex"""
        try:
            if not os.path.isdir(self.logs_list["bad_raw"]):
                os.makedirs(self.logs_list["bad_raw"])

            if not os.path.isdir(self.logs_list["good_raw"]):
                os.makedirs(self.logs_list["good_raw"])

        except OSError as er:
            self.logger.log(file_obj, 'Error while creating GoodBadDirs: %s' % er)
            raise OSError

    def validationRawColumns(self, NumberOfColumns, file_obj):
        """Description: Previously that files are added to the good raw, for which file name validated
        Here we are validating the Number of column in files and will move them to the bad folder if columns does not varifies
        """
        try:
            for file in os.listdir(self.logs_list["good_raw"]):
                csv = pd.read_csv(os.path.join(self.logs_list["good_raw"], file))
                if csv.shape[1] == NumberOfColumns:
                    pass
                else:
                    shutil.move(os.path.join(self.logs_list["good_raw"], file), self.logs_list["bad_raw"])
                    self.logger.log(file_obj, "Invalid Column Length for the file. Bad Raw Folder: %s" % file)
            self.logger.log(file_obj, "Column Length Validation END")
        except Exception as e:
            self.logger.log(file_obj, "Error Occurred (validationRawColumns): %s" % e)
            raise e

    def checkIsNAinWholeColumn(self, file_obj):
        """Description: Extra Validation: Validate if whole column has missing data """
        try:
            
            for file_name in os.listdir(self.logs_list["good_raw"]):
                df = pd.read_csv(os.path.join(self.logs_list["good_raw"], file_name))
                count = 0
                for column in df:
                    if (len(df[column]) - df[column].count()) == len(df[column]):
                        count = count + 1
                        shutil.move(os.path.join(self.logs_list["good_raw"], file_name), self.logs_list["bad_raw"])
                        self.logger.log(file_obj,
                                        'A Empty column found for file: %s, file moved to bad_raw folder' % file_name)
                        break
                if count == 0:
                    df.to_csv(os.path.join(self.logs_list["good_raw"], file_name), index=None, header=True)
            self.logger.log(file_obj, 'Missing Value validation END.')

        except Exception as e:
            self.logger.log(file_obj, 'Error Occurred while checking missing value: %s' % e)
            raise e

    def moveBadFilestoArchiveBad(self, file_obj):
        """Description: Deletes the Bad folder directory and & store in Archive Bad """
        time_now = datetime.now()
        date_now = time_now.date()
        time = time_now.strftime('%H%M%S')

        try:
            if os.path.isdir(self.logs_list["bad_raw"]):
                path = self.logs_list["archive_bad"]
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = self.logs_list["archive_bad"]+'/BadData_' + str(date_now) + "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)

                files = os.listdir(self.logs_list["bad_raw"])
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(os.path.join(self.logs_list["bad_raw"], f), dest)

                self.logger.log(file_obj, 'Bad Files moved to archive')
                if os.path.isdir(self.logs_list["bad_raw"]):
                    shutil.rmtree(self.logs_list["bad_raw"])
                self.logger.log(file_obj, 'Deleted Bad Data Folder.')

        except Exception as er:
            self.logger.log(file_obj, 'Error while moving Bad Files to archive : %s' % er)
            raise er