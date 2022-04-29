import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
from sklearn.impute import KNNImputer


class Preprocessor:
    """ This class will use to clean and transform data ready for training """

    def __init__(self, file_obj, log_obj):
        self.file_obj = file_obj
        self.logger = log_obj

    def enocdeCategoricalvalues(self, data_inp):
        data_inp['class'] = data_inp['class'].map({
            'Lodgepole_Pine': 0,
            'Spruce_Fir': 1,
            'Ponderosa_Pine': 2,
            'Krummholz': 3,
            'Douglas_fir': 4,
            'Aspen': 5,
            'Cottonwood_Willow': 6
        })
        return data_inp

    def handleImbalanceDataset(self, X, Y):
        """ Synthetic Minority Over-sampling """
        sample = SMOTE()
        X, Y = sample.fit_resample(X, Y)
        return X, Y

    def scaleData(self, feature_data):
        """ Performing feature scaling """
        scaler = StandardScaler()
        num_columns = ['elevation', 'aspect', 'slope', 'horizontal_distance_to_hydrology',
                       'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
                       'Horizontal_Distance_To_Fire_Points']
        num_data = feature_data[num_columns]
        cat_data = feature_data.drop(num_columns, axis=1)
        scaled_data = scaler.fit_transform(num_data)

        num_data = pd.DataFrame(scaled_data, columns=num_data.columns, index=num_data.index)
        prepare_data = pd.concat([num_data, cat_data], axis=1)
        self.logger.log(self.file_obj, 'Features Scaling Completed')
        return prepare_data
