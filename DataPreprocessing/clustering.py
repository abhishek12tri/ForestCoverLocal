import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from kneed import KneeLocator
from fileOperations.fileMethods import FileMethods


class KMeansClustering:
    """ The class will be used to handle all kinds of clustering methodologies
    for the dataset (KMeans) """

    def __init__(self, file_object, logger):
        self.numberCluster = None
        self.file_object = file_object
        self.logger = logger

    def elbow_plot(self, features):
        self.logger.log(self.file_object, 'Finding Optimum Clustering Number')
        wcss = []
        try:
            for i in range(2, 12):
                meanobj = KMeans(n_clusters=i, init='k-means++', random_state=32)
                """ Fitting the Data """
                meanobj.fit(features)
                wcss.append(meanobj.inertia_)

            print(wcss)
            plt.plot(range(2, 12), wcss)
            plt.title('Elbow Plotting')
            plt.xlabel('No. of clusters')
            plt.ylabel('WCSS')
            # plt.show()
            plt.savefig('Preprocessing_Data/K-Means_Elbow1.PNG')

            self.numberCluster = KneeLocator(range(2, 12), wcss, curve='convex', direction='decreasing')
            self.logger.log(self.file_object, "Cluster Number = %s" % self.numberCluster)

            return self.numberCluster.knee

        except Exception as ex:
            self.logger.log(self.file_object, 'Error in Elbow Method')
            raise ex

    def create_clusters(self, features, clusterNumber):
        self.logger.log(self.file_object, 'Entered KMeans Clustering')
        try:
            kmean = KMeans(n_clusters=clusterNumber, init='k-means++', random_state=32)
            """ Dividing data into Clusters """
            y_means = kmean.fit_predict(features)
            fileoper_obj = FileMethods(self.file_object, self.logger)
            """ Saving KMean Model """
            save_model = fileoper_obj.save_model(kmean, 'KMeans')
            """ Adding Cluster data in Features """
            features['cluster'] = y_means
            self.logger.log(self.file_object, 'Successfully created Cluster: ' + str(self.numberCluster))
            return features
        except Exception as ex:
            self.logger.log(self.file_object, 'Error in creating clusters ' + str(ex))
            raise ex
