from scipy import sparse
import numpy as np
import math
from sklearn.cluster import KMeans
import copy
import pickle as pi

class Clustering_Algorithms:

    def k_means(self, X, n_clusters):
        kmeans = KMeans(n_clusters=n_clusters, random_state=1231)
        return kmeans.fit(X).labels_

    def spectral_clustering(self, data, c):

        n = len(data.img_ids)

        laplacian = sparse.lil_matrix((n, n), dtype=float)

        # Symmetric normalized Laplacian
        for i in range(n):
            for j in range(data.k):
                x = data.graph[i][j]
                if i == j:
                    laplacian[i, j] = 1 #data.degree_mat[i]
                elif data.adjacency_mat[i, x] == 1:
                    d = -1/math.sqrt(data.degree_mat[i] * data.degree_mat[x])
                    laplacian[i, x] = d

        eig_val, eig_vect = sparse.linalg.eigs(laplacian, c)
        X = eig_vect.real
        rows_norm = np.linalg.norm(X, axis=1, ord=2)
        Y = (X.T / rows_norm).T
        labels = self.find_converging_centroid(Y, c)

        return labels

    def find_converging_centroid(self, data, k):
        clusters = np.zeros(data.shape[0])
        C = np.random.uniform(low=np.min(data), high=np.max(data), size=(k, data.shape[1]))
        C_previous = np.zeros(C.shape)
        change_in_centroid = self.euclidean_distance(C, C_previous, None)

        while change_in_centroid != 0:
            empty_cluster = False
            empty_cluster_index = 0
            biggest_cluster = 0
            single_biggest_cluster = []
            biggest_cluster_index = 0
            # CLASSIFY
            for i in range(data.shape[0]):
                distance_X_allC = self.euclidean_distance(data[i], C)
                cluster_index = np.argmin(distance_X_allC)
                clusters[i] = cluster_index
            C_previous = np.array(C, copy=True)
            # RECENTER
            for i in range(k):
                x_of_single_cluster = []
                for h in range(data.shape[0]):
                    if clusters[h] == i:
                        x_of_single_cluster.append(data[h])
                if len(x_of_single_cluster) == 0:
                    empty_cluster = True
                    empty_cluster_index = i
                    print("empty cluster found")
                else:
                    C[i] = np.mean(x_of_single_cluster, axis=0)
                if biggest_cluster < len(x_of_single_cluster):
                    biggest_cluster = len(x_of_single_cluster)
                    single_biggest_cluster = copy.copy(x_of_single_cluster)
                    biggest_cluster_index = i
            if empty_cluster:
                # divide the biggest cluster into two equal cluster
                list1 = single_biggest_cluster[:int(len(single_biggest_cluster) / 2)]
                list2 = single_biggest_cluster[int(len(single_biggest_cluster) / 2):]
                C[biggest_cluster_index] = np.mean(list1, axis=0)
                C[empty_cluster_index] = np.mean(list2, axis=0)
            change_in_centroid = self.euclidean_distance(C, C_previous, None)

        clusters = clusters.astype(np.int)
        clusters = clusters.tolist()
        return clusters

    def euclidean_distance(self, x, y, along=1):
        # return scipy.spatial.distance.cdist(x,y,'euclidean')
        return np.linalg.norm(x - y, axis=along)

    def normalised_cut(self, data, c):

        nodes = [i for i in range(len(data.img_ids))]
        clusters = []

        self._normalised_cut_rec(data, nodes, c, clusters)
        return clusters

    def _normalised_cut_rec(self, data, nodes, c, clusters):

        if c < 2:
            clusters.append(nodes)
            return
        if len(clusters) == c-1:
            clusters.append(nodes)
            return
        if len(clusters) == c:
            return

        n = len(nodes)

        laplacian = sparse.lil_matrix((n, n), dtype=float)

        for i in range(len(nodes)):
            e = nodes[i]
            for j in range(data.k):
                x = data.graph[e][j]
                if x not in nodes:
                    continue
                f = nodes.index(x)
                if e == x:
                    laplacian[i, i] = 1  # data.degree_mat[i]
                elif data.adjacency_mat[e, x] == 1:
                    d = -1 / math.sqrt(data.degree_mat[e] * data.degree_mat[x])
                    laplacian[i, f] = d

        eig_val, eig_vec = np.linalg.eig(laplacian.todense())
        min_idx = -1
        min_val = 1000
        sec_min_idx = -1
        sec_min_val = 1000
        for idx, e in enumerate(eig_val.real):
            if e < min_val:
                sec_min_idx = min_idx
                sec_min_val = min_val
                min_idx = idx
                min_val = e
            elif e < sec_min_val:
                sec_min_val = e
                sec_min_idx = idx

        y = eig_vec[sec_min_idx]
        y = y.real

        cluster1 = []
        cluster2 = []
        for i in range(y.shape[1]):
            if y[0, i] >= 0:
                cluster1.append(nodes[i])
            else:
                cluster2.append(nodes[i])

        clusters.append(cluster1)
        clusters.append(cluster2)

        largest_cluster_size = 0
        largest_cluster_idx = -1

        for i in range(len(clusters)):
            if len(clusters[i]) > largest_cluster_size:
                largest_cluster_size = len(clusters[i])
                largest_cluster_idx = i


        next_cluster = clusters[largest_cluster_idx]
        del clusters[largest_cluster_idx]
        self._normalised_cut_rec(data, next_cluster, c, clusters)