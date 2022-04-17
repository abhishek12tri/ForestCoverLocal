from Training_Raw_data_validation.rawValidation import Raw_Data_validation
from DataTransform_Training.DataTransformation import dataTransform
from DataTypeValidation_Insertion_Training.DataTypeValidation import dBOperation
from application_logging.logger import App_Logger


class train_validation:
    def __init__(self, path):
        self.raw_data = Raw_Data_validation(path)
        self.dataTransform = dataTransform()
        self.dBOperation = dBOperation()
        self.file_object = open("Training_Logs/Training_Main_Log.txt", 'a+')
        self.log_writer = App_Logger()

    def train_validation(self):
        try:
            self.log_writer.log(self.file_object, 'Start of Validation on files for training!!')
            """extracting values from prediction schema"""
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberOfColumns = self.raw_data.values_from_schema()
            """getting the regex defined to validate filename"""
            regex_creation = self.raw_data.manual_regex_creation()
            """validating filenames and columns of prediction files"""
            self.raw_data.validationRawFileName(regex_creation, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            self.raw_data.validationRawColumns(NumberOfColumns)


            
            return LengthOfDateStampInFile
        except Exception as e:
            return e
