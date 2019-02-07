import numpy as np
import heapq
from sklearn.utils import shuffle

class KNN:
    def __init__(self):
        pass

    def train_model(self, X, Y):
        self.X = X
        self.Y = Y

    def find_k_nearest_friends(self, X_test, K):
        # values (priority, task) min heap
        k_neigbours = []
        for i in range(len(self.X)):
            val = np.sqrt(np.sum(np.square(X_test-self.X[i,:])))
            if len(k_neigbours)>= K:
                del k_neigbours[K-1]
            heapq.heappush(k_neigbours, (val, i))

        class_dict = {}
        for i in range(K):
            class_dict[self.Y[k_neigbours[i][1]]] = class_dict.get(self.Y[k_neigbours[i][1]], 0)+1
        return class_dict

    def classify_me(self, X_test, K):
        class_dict = self.find_k_nearest_friends(X_test, K)
        max_val = -1
        max_key = -1
        for key, val in class_dict.items():
            if val > max_val:
                max_val = val
                max_key = key
        return max_key


class WeightedKNN:
    def __init__(self):
        pass

    def train_model(self, X, Y):
        self.X = X
        self.Y = Y

    def find_k_nearest_friends(self, X_test):
        class_dict = {}
        for i in range(len(self.X)):
            val = np.sum(np.square(X_test-self.X[i,:]))
            class_dict[self.Y[i]] = class_dict.get(self.Y[i], 0.0)+(1/val)
        return class_dict

    def classify_me(self, X_test):
        class_dict = self.find_k_nearest_friends(X_test)
        max_val = -1.0
        max_key = -1.0
        for key, val in class_dict.items():
            if val > max_val:
                max_val = val
                max_key = key
        return max_key




