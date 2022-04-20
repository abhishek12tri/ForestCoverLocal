import os
import shutil
import re
import json
import pandas as pd
from datetime import datetime
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
        """Previously that files are added to the good raw, for which file name validated
        Here we are validating the Number of column in files and will move them to the bad folder if columns does not varifies
        """
        try:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Column Length Validation START")
            for file in os.listdir(self.raw_validated + self.good_raw):
                csv = pd.read_csv(self.raw_validated + self.good_raw + file)
                if csv.shape[1] == NumberOfColumns:
                    pass
                else:
                    shutil.move(self.raw_validated + self.good_raw + file, self.raw_validated + self.bad_raw)
                    self.logger.log(f, "Invalid Column Length for the file. Bad Raw Folder: %s" % file)
            self.logger.log(f, "Column Length Validation END")
        except OSError:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occurred while moving the file :: %s" % OSError)
            f.close()
            raise OSError
        except Exception as e:
            f = open("Training_Logs/columnValidationLog.txt", 'a+')
            self.logger.log(f, "Error Occurred:: %s" % e)
            f.close()
            raise e
        f.close()

    def checkIsNAinWholeColumn(self):
        """Extra Validation: Validate if whole column has missing data """
        try:
            file = open('Training_Logs/missingValuesInColumn.txt', 'a+')
            self.logger.log(file, 'Missing Value validation START.')
            for file_name in os.listdir(self.raw_validated + self.good_raw):
                df = pd.read_csv(self.raw_validated + self.good_raw + file_name)
                count = 0
                for column in df:
                    if (len(df[column]) - df[column].count()) == len(df[column]):
                        count = count + 1
                        shutil.move(self.raw_validated + self.good_raw + file_name, self.raw_validated + self.bad_raw)
                        self.logger.log(file,
                                        'A Empty column found for file: %s, file moved to bad_raw folder' % file_name)
                        break
                if count == 0:
                    df.to_csv(self.raw_validated + self.good_raw + file_name, index=None, header=True)
            self.logger.log(file, 'Missing Value validation END.')
            file.close()

        except OSError as osr:
            file = open('Training_Logs/missingValuesInColumn.txt', 'a+')
            self.logger.log(file, 'Error Occurred while checking missing value: %s' % osr)
            file.close()
            raise osr

        except Exception as e:
            file = open('Training_Logs/missingValuesInColumn.txt', 'a+')
            self.logger.log(file, 'Error Occurred while checking missing value: %s' % e)
            file.close()
            raise e

    def moveBadFilestoArchiveBad(self):
        """ Deletes the Bad folder directory and & store in Archive Bad """
        time_now = datetime.now()
        date_now = time_now.date()
        time = time_now.strftime('%H%M%S')

        try:
            if os.path.isdir(self.raw_validated + self.bad_raw):
                path = "TrainingArchiveBadData"
                if not os.path.isdir(path):
                    os.makedirs(path)
                dest = 'TrainingArchiveBadData/BadData_' + str(date_now) + "_" + str(time)
                if not os.path.isdir(dest):
                    os.makedirs(dest)

                files = os.listdir(self.raw_validated + self.bad_raw)
                for f in files:
                    if f not in os.listdir(dest):
                        shutil.move(self.raw_validated + self.bad_raw + f, dest)
                file = open('Training_Logs/GeneralLog.txt', 'a+')
                self.logger.log(file, 'Bad Files moved to archive')
                if os.path.isdir(self.raw_validated + self.bad_raw):
                    shutil.rmtree(self.raw_validated + self.bad_raw)
                self.logger.log(file, 'Deleted Bad Data Folder.')
                file.close()

        except Exception as er:
            file = open('Training_Logs/GeneralLog.txt', 'a+')
            self.logger.log(file, 'Error while moving Bad Files to archive : %s' % er)
            file.close()
            raise er
