import sqlite3
from datetime import datetime
import os
import shutil
import re
import json
# import pandas as pd
from application_logging.logger import App_Logger


class Raw_Data_validation:
    """This class is used for validation Dataset"""

    def __init__(self, path):
        self.BatchDirectory = path
        self.schema_path = 'schema_training.json'
        self.logger = App_Logger()

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
            message = "LengthOfDateStampInFile:: %s" % LengthOfDateStampInFile + "\t LengthOfTimeStampInFile:: %s" % LengthOfTimeStampInFile + "\t NumberofColumns:: %s" % NumberOfColumns+"\n"
            self.logger.log(file, message)
            file.close()

        except ValueError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message = 'ValueError: value are not found inside schema_training.json \n'
            self.logger.log(file, message)
            file.close()
            raise ValueError

        except KeyError:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            message = 'KeyError: Key value error incorrect key passed \n'
            self.logger.log(file, message)
            file.close()
            raise KeyError

        except Exception as e:
            file = open("Training_Logs/valuesfromSchemaValidationLog.txt", 'a+')
            self.logger.log(file, str(e)+' \n')
            file.close()
            raise e

        return LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberOfColumns

    def manual_regex_creation(self):
        return "['forest_cover']+['\_']+[\d_]+[\d]+\.csv"

    def validationRawFileName(self, regex, LengthOfDateStampInFile, LengthOfTimeStampInFile):
        '''Description: This function validates the input file nams CSV as per decided in schema.'''
        self.deleteExistingBadDataFolder()
        #self.deleteExistingGoodDataFolder()

    def deleteExistingBadDataFolder(self):
        '''Used to delete the existing Bad Data Folder.'''
        try:
            path = 'Training_Raw_files_validated/'
            if(os.path.isdir(path+'Bad_Raw/')):
                shutil.rmtree(path+'Bad_Raw/')
                file = open("training")

        except OSError as e:
            pass



    def deleteExistingGoodDataFolder(self):
        '''Used to delete the existing Good data Folder'''
        pass
