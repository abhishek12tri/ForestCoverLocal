"""
Author: Abhishek
Purpose: Handles training functionalities.
"""
import os
from App_logging.logger import App_Logger
from log_files import logs_list
from DataIngestion.ingestion_operation import Ingestion
from DataPreprocessing.preprocessing import Preprocess
from DataPreprocessing.clustering import KMeansClustering
from sklearn.model_selection import train_test_split
from Operational.tuner import Model_Finder
from Operational.model_opeartion import FileOperation


class trainModel:
    """Handles all training model related functionalities."""
    def __init__(self) -> None:
        self.logger = App_Logger()
        self.log_list = logs_list()
        self.file_obj = open(self.log_list["model_train"], 'a+')
        self.logger.log(self.file_obj, "-"*20)

    def training_model(self):
        self.logger.log(self.file_obj, "Model Training")
        try:
            training_data = Ingestion().get_training_data(self.file_obj)

            """Data preprocessing."""
            preprocess = Preprocess()
            preprocess.encode_categorical(training_data, self.file_obj)

            X = training_data.drop(["class"], axis=1)
            Y = training_data["class"]

            X, Y = preprocess.handleImbalanceDataset(X, Y, self.file_obj)
            
            kmeans = KMeansClustering()
            num_clusters = kmeans.elbow_plot(X, self.file_obj)
            
            """Data partition based on clusters."""
            X = kmeans.create_clusters(X, num_clusters, self.file_obj)
            X["Labels"] = Y

            list_cluster = X["Cluster"].unique()

            self.logger.log(self.file_obj, "Start: ML algo for each cluster.")
            """Best ML Algorithm fit in each cluster."""
            for i in list_cluster:
                cluster_data = X[X["Cluster"]==i]

                cluster_features = cluster_data.drop(["Labels", "Cluster"], axis = 1)
                cluster_label = cluster_data["Labels"]

                """Data Splitting into train and test set."""
                X_train, X_test, y_train, y_test = train_test_split(
                    cluster_features, cluster_label, test_size= 1/3, random_state=42
                )

                X_train = preprocess.scaleData(X_train, self.file_obj)
                X_test = preprocess.scaleData(X_test, self.file_obj)

                model_finder = Model_Finder()
                finder_resp = model_finder.get_best_model(X_train, y_train, X_test, y_test, self.file_obj)

                file_op = FileOperation()
                file_op.save_model(finder_resp["model"], os.path.join(self.log_list["model_dir"],  finder_resp["name"]+"_"+str(i)), self.file_obj)
            self.logger.log(self.file_obj, "Training Completed")
            self.file_obj.close()

        except Exception as e:
            self.logger.log(self.file_obj, "Error in training: %s"%e)
            raise e

