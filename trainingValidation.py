"""
Author: Abhishek
Purpose: Dataset validation program
"""
from RawValidation.validation import DataValidation
from App_logging.logger import App_Logger
from log_files import logs_list
from DataTransformation.train_transform import TrainTranformation
from DataTypeDB.training_db import DBOperation


class trainValidation:
    def __init__(self, path) -> None:
        self.validation = DataValidation(path)
        self.logger = App_Logger()
        self.logs_list = logs_list()
        self.file_obj = open(self.logs_list["train_log"], "a+")
        self.logger.log(self.file_obj, "-"*20)
        self.transform = TrainTranformation()
        self.dbOperation = DBOperation()

    def train_validate(self):
        try:
            self.logger.log(self.file_obj, "Start Validation on files")

            """Raw files validation."""
            LengthOfDate, LengthOfTime, column_names, NoOfColumn = self.validation.rawSchemaValues(self.file_obj)
            file_name_regex = self.validation.filename_checker()
            self.validation.validate_raw_files(file_name_regex, LengthOfDate, LengthOfTime, self.file_obj)

            self.validation.validationRawColumns(NoOfColumn, self.file_obj)
            self.validation.checkIsNAinWholeColumn(self.file_obj)

            self.logger.log(self.file_obj, "Raw Validation Complete")

            self.transform.addQuotesToString(self.file_obj)
            self.logger.log(self.file_obj, "Data Transformation Complete")

            self.dbOperation.createTable("Training", column_names, self.file_obj)
            self.dbOperation.insert_into_table("Training", self.file_obj)
            
            self.logger.log(self.file_obj, "Insert DB Complete.")

            self.validation.deleteExistingGoodDataFolder(self.file_obj)
            self.validation.moveBadFilestoArchiveBad(self.file_obj)
            self.logger.log(self.file_obj, "Deleted good folder and bad to archieve.")

            self.dbOperation.selectingDataToCSV("Training",self.file_obj)
            self.logger.log(self.file_obj, "Extracting CSV file from table.")
            self.file_obj.close()

        except Exception as e:
            self.logger.log(self.file_obj, str(e))
            self.file_obj.close()
            raise e



