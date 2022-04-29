from data_ingestion import data_loader
from DataPreprocessing.preprocessing import Preprocessor
from DataPreprocessing.clustering import KMeansClustering
from sklearn.model_selection import train_test_split
from application_logging import logger
from BestModelFinder.modelTuner import ModelFinder
from fileOperations.fileMethods import FileMethods


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

            self.logger.log(self.file_object, 'Train Test Split')
            X = data_inp.drop('class', axis=1)
            Y = data_inp['class']

            """ Balancing Dataset using SMOTE Resampling """
            X, Y = preprocessor.handleImbalanceDataset(X, Y)
            """ Clustering """
            cluster = KMeansClustering(self.file_object, self.logger)
            clusterNumber = cluster.elbow_plot(X)

            X = cluster.create_clusters(X, clusterNumber)
            """ Now dataset has 2 additional columns- Cluster and label """
            X['label'] = Y
            cluster_list = X['cluster'].unique()
            print('cluster_list')
            print(cluster_list)

            """parsing all the clusters and looking for the best ML algorithm to fit on individual cluster"""
            for i in cluster_list:
                cluster_data = X[X['cluster'] == i]

                """ Features and labels columns """
                cls_features = cluster_data.drop(['cluster', 'label'], axis=1)
                cls_labels = cluster_data['label']

                X_train, X_test, Y_train, Y_test = train_test_split(cls_features, cls_labels, test_size=(1 / 3),
                                                                    random_state=32)
                print('Feature Shapes')
                print(X_train)
                print(X_test)
                print(Y_train)
                print(Y_test)

                X_train = preprocessor.scaleData(X_train)
                X_test = preprocessor.scaleData(X_test)

                """ Getting best model per cluster """
                model_finder = ModelFinder(self.file_object, self.logger)
                best_model_name, best_model = model_finder.try_best_model(X_train, X_test, Y_train, Y_test)

                fileOperations = FileMethods(self.file_object, self.logger)
                fileOperations.save_model(best_model, best_model_name+str(i))

            self.logger.log(self.file_object, 'Training Successfully END')
            self.file_object.close()

        except Exception as er:
            self.logger.log(self.file_object, 'Error in Training: %s' % er)
            self.file_object.close()
            raise er