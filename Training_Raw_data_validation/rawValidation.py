import sqlite3
from datetime import datetime
import os
import shutil
import re
import json
import pandas as pd
from application_logging.logger import App_Logger


class Raw_Data_validation:
    """This class is used for validation Dataset"""

    def __init__(self, path):
        self.BatchDirectory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()
        self.raw_validated = 'Training_Raw_files_validated/'
        self.good_raw = 'Good_Raw/'
        self.bad_raw = 'Bad_Raw/'
        self.training_batch = 'Training_Batch_Files/'

    def values_from_schema(self):
        try:
            with open(self.schema_path, 'r') as f:
                dic = json.load(f)
            f.close()
            pattern = dic['SampleFileName']
            LengthOfDateStampInFile = dic['LengthOfDateStampInFile']
            LengthOfTimeStampInFile = dic['LengthOfTimeStampInFile']
            column_names = dic['ColName']
            NumberOfColumns = dic['NumberofColumns']

            file = open('Training_Logs/valuesfromSchemaValidationLog.txt', 'a+')
            message = "LengthOfDateStampInFile:: %s" % LengthOfDateStampInFile + "\t LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile + "\t NumberofColumns:: %s" % NumberOfColumns
            self.logger.log(file, message)
            file.close()

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message = 'ValueError: value are not found inside schema_training.json'
            self.logger.log(file, message)
            file.close()
            raise ValueError

        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message = 'KeyError: Key value error incorrect key passed'
            self.logger.log(file, message)
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e))
            file.close()
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberOfColumns

    def manual_regex_creation(self):
        return "['forest_cover']+['\_']+[\d_]+[\d]+\.csv"

    def validationRawFileName(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        """Description: This function validates the input file names CSV as per decided in schema."""
        self.deleteExistingBadDataFolder()
        self.deleteExistingGoodDataFolder()
        self.createGoodBadDataFolder()
        onlyFiles = [f for f in os.listdir(self.BatchDirectory)]
        try:
            file = open('Training_Logs/nameValidationLog.txt', 'a+')
            for filename in onlyFiles:
                if re.match(regex, filename):
                    splitAtDot = re.split('.csv', filename)
                    splitAtDot = re.split('_', splitAtDot[0])
                    if len(splitAtDot[2]) == LengthOfDateStampInFile:
                        if len(splitAtDot[3]) == LengthOfTimeStampInFile:
                            shutil.copy(self.training_batch + filename, self.raw_validated + self.good_raw)
                            self.logger.log(file, 'Valid file name: %s' % filename)
                        else:
                            shutil.copy(self.training_batch + filename, self.raw_validated + self.bad_raw)
                            self.logger.log(file, 'Invalid file name: %s' % filename)
                    else:
                        shutil.copy(self.training_batch + filename, self.raw_validated + self.bad_raw)
                        self.logger.log(file, 'Invalid file name: %s' % filename)
                else:
                    shutil.copy(self.training_batch + filename, self.raw_validated + self.bad_raw)
                    self.logger.log(file, 'Invalid file name: %s' % filename)
            file.close()
        except Exception as e:
            file = open('Training_Logs/nameValidationLog.txt', 'a+')
            self.logger.log(file, 'Error occurred in validating %s' % e)
            file.close()
            raise e

    def deleteExistingBadDataFolder(self):
        """Used to delete the existing Bad Data Folder."""
        try:
            if os.path.isdir(self.raw_validated + self.bad_raw):
                shutil.rmtree(self.raw_validated + self.bad_raw)
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file, 'Bad data raw deleted from folder')
                file.close()
        except OSError as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, 'Bad file deletion error: %s' % e)
            file.close()
            raise OSError

    def deleteExistingGoodDataFolder(self):
        """Used to delete the existing Good data Folder"""
        path = 'Training_Raw_files_validated/'
        try:
            if os.path.isdir(self.raw_validated + self.good_raw):
                shutil.rmtree(self.raw_validated + self.good_raw)
                file = open("Training_Logs/GeneralLog.txt", 'a+')
                self.logger.log(file, 'Good file deleted from folder')
                file.close()
        except OSError as e:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, 'Good file deletion error: %s' % e)
            file.close()
            raise OSError

    def createGoodBadDataFolder(self):
        """Used to create data for Good data file: that will pass the CSV file name with Regex"""
        try:
            path = os.path.join(self.raw_validated + self.good_raw)
            if not os.path.isdir(path):
                os.makedirs(path)
            path = os.path.join(self.raw_validated + self.bad_raw)
            if not os.path.isdir(path):
                os.makedirs(path)
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, 'Good Bad Directory created successfully')
            file.close()
        except OSError as er:
            file = open("Training_Logs/GeneralLog.txt", 'a+')
            self.logger.log(file, 'Error while creating GoodBadDirs: %s' % er)
            file.close()
            raise OSError

    def validationRawColumns(self, NumberOfColumns):
        try:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Column Length Validation Started!!")
            for file in os.listdir('Training_Raw_files_validated/Good_Raw/'):
                csv = pd.read_csv("Training_Raw_files_validated/Good_Raw/" + file)
                if csv.shape[1] == NumberOfColumns:
                    pass
                else:
                    shutil.move("Training_Raw_files_validated/Good_Raw/" + file, "Training_Raw_files_validated/Bad_Raw")
                    self.logger.log(f, "Invalid Column Length for the file!! File moved to Bad Raw Folder :: %s" % file)
            self.logger.log(f, "Column Length Validation Completed!!")
        except OSError:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occured:: %s" % e)
            f.close()
            raise e
        f.close()

