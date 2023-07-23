"""
Author: Abhishek
Purpose: Handles training clustering work
"""
from App_logging.logger import App_Logger
from sklearn.cluster import KMeans
import matplotlib.pyplot as plt
from log_files import logs_list
from kneed import KneeLocator
from Operational.model_opeartion import FileOperation


class KMeansClustering:
    def __init__(self) -> None:
        self.logger = App_Logger()
        self.logs_list = logs_list()


    def elbow_plot(self, data, file_obj):
        """Description: Decides the optimum number of clusters to the data."""
        wcss = []
        try:
            for i in range(1, 11):
                kmeans = KMeans(
                    n_clusters=i,
                    init="k-means++",
                    random_state=42
                )
                kmeans.fit(data)
                wcss.append(kmeans.inertia_)
            plt.plot(range(1, 11), wcss)
            plt.title("Elbow Method")
            plt.xlabel("No. of cluster")
            plt.ylabel("WCSS")
            plt.savefig(self.logs_list["elbow_file"])

            locator = KneeLocator(range(1, 11), wcss, curve="convex", direction="decreasing")
            self.logger.log(file_obj, "Clusters: "+str(locator.knee))
            return locator.knee

        except Exception as e:
            self.logger.log(file_obj, "Error elbow plot: %s"%e)
            raise e
        
    
    def create_clusters(self, data, num_cluster, file_obj):
        """Description: Create new daatframe based on clustrs."""
        try:
            kmeans = KMeans(
                n_clusters=num_cluster,
                init="k-means++",
                random_state=42
            )

            y_means = kmeans.fit_predict(data)

            file_operation = FileOperation()
            file_operation.save_model(kmeans, self.logs_list["kmeans_model"], file_obj)

            data["Cluster"] = y_means

            self.logger.log(file_obj, "Created data clusters: "+ str(num_cluster))
            return data
        
        except Exception as e:
            self.logger.log(file_obj, "Exception create cluster:"+ str(e))
            raise e