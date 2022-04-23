import pandas as pd
import numpy as np
from sklearn.impute import KNNImputer


class Preprocessor:
    """ This class will use to clean and transform data ready fo training """

    def __init__(self, file_obj, log_obj):
        self.file_obj = file_obj
        self.logger = log_obj

    def enocdeCategoricalvalues(self, data_inp):
        # data_inp['class'] = data_inp['class'].map({
        #
        # })
        print(data_inp['class'].unique())
        return data_inp