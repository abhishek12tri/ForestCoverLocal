import pandas as pd


class dataGetter:
    """ Class Used to Load the data from File """

    def __init__(self, file_obj, log_obj):
        self.dataFrame = None
        self.file_obj = file_obj
        self.log_obj = log_obj
        self.training_file = 'Training_FileFromDB/InputFile.csv'

    def getData(self):
        self.log_obj.log(self.file_obj, 'Getting Data from file START')
        try:
            self.dataFrame = pd.read_csv(self.training_file)
            self.log_obj.log(self.file_obj, 'Data loaded successfully')
            return self.dataFrame
        except Exception as ex:
            self.log_obj.log(self.file_obj, 'Error in data loading: %s' % ex)
            raise ex
