import pickle
import os
import shutil


class FileMethods:
    """ This class handles all the file operations """

    def __init__(self, file_obj, log_obj):
        self.file_object = file_obj
        self.logger = log_obj
        self.model_directory = 'models/'

    def save_model(self, data_obj, file_name):
        """ Method use to save the model """
        self.logger.log(self.file_object, 'Saving the Model: ' + file_name)
        try:
            path = os.path.join(self.model_directory, file_name)
            """ Remove if path already path created """
            if os.path.isdir(path):
                shutil.rmtree(self.model_directory)
                os.makedirs(path)
            else:
                os.makedirs(path)
            """ Write the file Object Now """
            with open(path + '/' + file_name + '.sav', 'wb') as f:
                pickle.dump(data_obj, f)
            self.logger.log(self.file_object, 'Model Saved: ' + file_name)
        except Exception as ex:
            self.logger.log(self.file_object, 'Error while saving the model: ' + str(ex))
            self.logger.log(self.file_object, 'Error Filename model: ' + file_name)
            raise ex
