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
        self.logger = App_Logger()
        self.trainingDB = 'Training'

    def train_validation(self):
        try:
            """ Data Validation START """
            # self.logger.log(self.file_object, 'Start of Validation on files for training!!')
            # """extracting values from prediction schema"""
            LengthOfDateStampInFile, LengthOfTimeStampInFile, column_names, NumberOfColumns = self.raw_data.values_from_schema()
            # """getting the regex defined to validate filename"""
            # regex_creation = self.raw_data.manual_regex_creation()
            # """validating filenames and columns of prediction files"""
            # self.raw_data.validationRawFileName(regex_creation, LengthOfDateStampInFile, LengthOfTimeStampInFile)
            # self.raw_data.validationRawColumns(NumberOfColumns)
            # self.raw_data.checkIsNAinWholeColumn()
            # self.logger.log(self.file_object, 'Validation Completed')
            """ Data Validation END """

            """ Data Transformation START """
            # self.logger.log(self.file_object, 'Data Transformation START')
            # self.dataTransform.addQuotesToStringValueinColumn()
            # self.logger.log(self.file_object, 'Data Transformation END')
            """ Data Transformation END """

            """ Perform Database Operations for training START """
            self.logger.log(self.file_object, 'Training database operations START')
            self.dBOperation.createTableDB(self.trainingDB, column_names)
            self.logger.log(self.file_object, 'Training table CREATED')

            self.dBOperation.insertionIntoGoodDB(self.trainingDB)
            print("insert complete")
            # self.logger.log(self.file_object, 'Table Data Insertion COMPLETED')
            # self.logger.log(self.file_object, 'Deletion Good Data Folder START')
            # self.raw_data.deleteExistingGoodDataFolder()
            self.logger.log(self.file_object, 'Deletion Good Data Folder END')
            # self.raw_data.moveBadFilestoArchiveBad()
            # self.logger.log(self.file_object, 'Moved Bad files to archive')
            # self.logger.log(self.file_object, 'Validation Operation completed.')
            self.dBOperation.selectdatafromtableintoCSV(self.trainingDB)
            self.file_object.close()
            """ Perform Database Operations for training END """

        except Exception as e:
            self.file_object.close()
            return e
