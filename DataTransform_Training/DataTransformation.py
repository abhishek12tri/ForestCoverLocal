import os
import pandas as pd
from application_logging.logger import App_Logger


class dataTransform:
    def __init__(self):
        self.goodDataPath = 'Training_Raw_files_validated/Good_Raw/'
        self.logger = App_Logger()

    def addQuotesToStringValueinColumn(self):
        """Used to convert all data type to string To avoid error in Data insertion operation"""
        quote_log = open('Training_Logs/addQuotesToStringValuesInColumn.txt', 'a+')
        try:
            goodfiles = [f for f in os.listdir(self.goodDataPath)]
            for file in goodfiles:
                df = pd.read_csv(self.goodDataPath + file)
                df['class'] = df['class'].apply(lambda x: "'" + str(x) + "'")
                df.to_csv(self.goodDataPath + file, index=None, header=True)
                self.logger.log(quote_log, 'Quote added for %s' % file)
        except Exception as e:
            self.logger.log(quote_log, 'Error in data Transformation: %s' % e)
            quote_log.close()
            raise e
        quote_log.close()
