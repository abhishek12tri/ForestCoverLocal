"""
Author: Abhishek
Purpose: Predict data from the model
"""
import os
import pandas as pd
from log_files import logs_list
from Operational.model_opeartion import FileOperation
from App_logging.logger import App_Logger
from PredictionValidate.rawValidation import RawValidate
from DataPreprocessing.preprocessing import Preprocess


class Predict:
    def __init__(self, path) -> None:
        self.path = path
        self.log_list = logs_list()
        self.file_obj = open(self.log_list["prediction"], "a+")
        self.logger = App_Logger()
        self.logger.log(self.file_obj, "-"*30)

    def predict_data(self):
        """
        Description: Covers prediction form the saved model.
        """
        try:
            validate = RawValidate(self.path)
            saved_data = validate.load_data(self.file_obj)
            process = Preprocess()
            prepare_data = process.scaleData(saved_data, self.file_obj)

            file_opr = FileOperation()
            cluster_model = file_opr.load_model(self.log_list["kmeans_model"]+".sav", self.file_obj)
            clusters = cluster_model.predict(prepare_data)
            prepare_data['clusters'] = clusters

            clusters = prepare_data["clusters"].unique()
            results = []
            for i in clusters:
                cluster_data = prepare_data[prepare_data["clusters"]==i]
                cluster_data = cluster_data.drop(["clusters"], axis=1)
                model_name = file_opr.find_correct_model(i, self.file_obj)
                if os.path.isfile(model_name):
                    pred_model = file_opr.load_model(model_name, self.file_obj)
                    pred_data = pred_model.predict(cluster_data)
                    label_data = file_opr.load_label_data(self.file_obj)
                    rev_label = {b: a for a, b in label_data.items()}
            
                    for each_key in pred_data:
                        try:
                            results.append(rev_label[each_key])
                        except Exception as e:
                            self.logger.log(self.file_obj, "Did not find the label "+str(rev_label[each_key]))
                            results.append(None)
            
            self.logger.log(self.file_obj, "Prediction Completed.")
            results = pd.DataFrame(results, columns=["Predictions"])
            pred_file = os.path.join(self.path, self.log_list["pred_file"])
            results.to_csv(pred_file, header=True, mode="a+")
            return pred_file

        except Exception as e:
            self.logger.log(self.file_obj, "Error in data prediction: "+str(e))
            raise e
