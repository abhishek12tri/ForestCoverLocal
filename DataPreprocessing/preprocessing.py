"""
Author: Abhishek
Purpose: Preprocess data functionality
"""
from App_logging.logger import App_Logger
from imblearn.over_sampling import SMOTE
from sklearn.preprocessing import StandardScaler
import pandas as pd


class Preprocess:
    def __init__(self) -> None:
        self.logger = App_Logger()

    def encode_categorical(self, data, file_obj):
        """Description: Labels categorical encoding."""
        try:
            arr_data = data["class"].unique()

            data_dict = {single_ele: index  for index, single_ele in enumerate(arr_data)}
            data["class"] = data["class"].map(data_dict)

            return data
        except Exception as e:
            self.logger.log(file_obj, "Error in label encoding: %s"%e)
            raise e
        
    def handleImbalanceDataset(self, X, Y, file_obj):
        """Description: Handles imbalanced data, prevent biasing."""
        try:
            sample = SMOTE()
            X, Y = sample.fit_resample(X, Y)

            return X, Y
        except Exception as e:
            self.logger.log(file_obj, "Error imbalanced: %s"%e)

    def scaleData(self, feature_data, file_obj):
        """ Performing feature scaling """
        try:
            scaler = StandardScaler()
            num_columns = ['elevation', 'aspect', 'slope', 'horizontal_distance_to_hydrology',
                        'Vertical_Distance_To_Hydrology', 'Horizontal_Distance_To_Roadways',
                        'Horizontal_Distance_To_Fire_Points']
            num_data = feature_data[num_columns]
            cat_data = feature_data.drop(num_columns, axis=1)
            scaled_data = scaler.fit_transform(num_data)

            num_data = pd.DataFrame(scaled_data, columns=num_data.columns, index=num_data.index)
            prepare_data = pd.concat([num_data, cat_data], axis=1)
            self.logger.log(file_obj, 'Features Scaling Completed')
            return prepare_data

        except Exception as e:
            self.logger.log(file_obj, 'Error in Features Scaling', e)
            raise e