from data_ingestion import data_loader
from DataPreprocessing.preprocessing import Preprocessor
from sklearn.model_selection import train_test_split
from application_logging import logger
import pandas as pd


class trainModel:
    """ Class used to train the Model """
    def __init__(self):
        self.logger = logger.App_Logger()
        self.file_object = open('Training_Logs/ModelTrainingLog.txt', 'a+')

    def trainingModel(self):
        self.logger.log(self.file_object, 'Model Training START')
        try:
            """ Data Collection """
            loader = data_loader.dataGetter(self.file_object, self.logger)
            data_inp = loader.getData()

            """ Data Preprocessing """
            preprocessor = Preprocessor(self.file_object, self.logger)
            data_inp = preprocessor.enocdeCategoricalvalues(data_inp)
            print(data_inp.head())
            print(data_inp.columns)
            print(pd.DataFrame(data_inp.elevation).head() )
            self.file_object.close()

        except Exception as er:
            self.logger.log(self.file_object, 'Error in Training: ' % er)
            self.file_object.close()
            raise er
        print('aasas')
