"""
Author: Abhishek
Purpose: Validate prediction data
"""
from PredictionValidate.rawValidation import RawValidate
from log_files import logs_list
from App_logging.logger import App_Logger
from PredictionValidate.predInsertion import dBOperation


class PredictionValidation:
    def __init__(self, path) -> None:
        self.path = path
        self.log_list = logs_list()
        self.file_obj = open(self.log_list["pred_log"], "a+")
        self.logger = App_Logger()
        self.logger.log(self.file_obj, "-"*35)
        self.raw_data = RawValidate(path)
        self.dbOperate = dBOperation()

    def prediction_validation(self):
        try:
            LenOfDate, LenOfTime, column_name, NumColumns = self.raw_data.valuesFromSchema(self.file_obj)
            regex_validate = self.raw_data.manual_regex_creation()
            self.raw_data.validate_file(regex_validate, LenOfDate, LenOfTime, self.file_obj)
            self.raw_data.validate_column_length(NumColumns, self.file_obj)
            self.raw_data.validateMissingValues(self.file_obj)
            self.logger.log(self.file_obj, "Raw data validated!")

            self.dbOperate.createTable(column_name, self.file_obj)
            self.dbOperate.insertIntoTable(self.path, self.file_obj)
            self.dbOperate.dataFromTableIntoCSV(self.path, self.file_obj)


        except Exception as e:
            self.logger.log(self.file_obj, "Error in prediction_validation: "+str(e))
            self.file_obj.close()

        