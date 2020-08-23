from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.preprocessing import MinMaxScaler
import numpy as np


class Clustering():
    datas = []
    n_clusters = 0
    labels = []
    dicts = {}

    def __init__(self, datas, features, is_scale=False):
        print("Initiating Clustering")
        self.set_data(datas, is_scale)
        print(f"Transforming data: {self.datas}")

        print("Calculating Optimal N")
        self.calculate_n()
        print("Optimal N: {self.n_clusters}")

        print("Calculating Clustering using Optimal N")
        self.labels = self.clustering()
        print("Cluster labels acquired: {labels}")

        print("Transforming Clustering Result")
        self.cluster_vector(datas, features)
        print("Transformed Clustering Result Acquired: {self.dicts}")

    def set_data(self, datas, is_scale):
        self.datas = np.array(datas)
        if is_scale:
            scaler = MinMaxScaler()
            scaler.fit(datas)
            self.datas = scaler.transform(datas)

    def calculate_n(self):
        max_silhouette = 0
        max_index = 0

        max_looping = len(self.datas)
        if max_looping > 100:
            max_looping = 100
        print(f"Looping for {max_looping}")

        for i in range(2, max_looping, 1):
            labels = self.clustering(i)
            silhouette = silhouette_score(self.datas, labels, metric='euclidean')
            print(f"Index {i} with silhouette {silhouette}")
            if silhouette > max_silhouette:
                max_silhouette = silhouette
                max_index = i
        self.n_clusters = max_index

    def clustering(self, n_clusters=None):
        kmeans = KMeans(n_clusters=n_clusters, init='k-means++', n_init=10, max_iter=50, random_state=0)
        if n_clusters is not None:
            kmeans.fit(self.datas)
        else:
            kmeans = KMeans(n_clusters=self.n_clusters, init='k-means++', n_init=10, max_iter=50, random_state=0)
            kmeans.fit_predict(self.datas)
        return kmeans.labels_

    def cluster_vector(self, vectors, features):
        clustered_vectorize = {}
        for cluster in range(self.n_clusters):
            vector_of_same_cluster = []
            for index in range(len(vectors)):
                if self.labels[index] == cluster:
                    vector_of_same_cluster.append(vectors[index])
            
            summarized_vector = np.sum(vector_of_same_cluster, axis=0)
            sorted_index = np.argsort(summarized_vector)

            words = []
            for word_idx in sorted_index[-3:]:
                words.append(features[word_idx])
            clustered_vectorize[cluster] = '-'.join(words)
        self.dicts = clustered_vectorize
