import numpy as np
import math

'''
From Near-Optimal Hashing Algorithms for
Approximate Nearest Neighbor in High Dimensions by  Alexandr Andoni and Piotr Indyk
Using LSH Euclidean Hash family
hr, b = floor((r·x + b)/w)
'''
class LSHIndex:

    def __init__(self, data, l, k, w):
        self.layers = l
        self.k = k
        self.w = w
        self._data = np.array(data)
        n = self._data.shape[0]
        c = self._data.shape[1]
        self.shifts = np.random.uniform(0, w,(l,k))
        self.dict_arr = [dict() for x in range(l)]
        self.random_proj_vectors = []
        for i in range(l):
            self.random_proj_vectors.append([])
            for j in range(k):
                self.random_proj_vectors[i].append([])
                vector = []
                for t in range(c):
                    vector.extend(np.random.normal(0,1,1))
                vector_hat = vector/np.linalg.norm(vector)
                self.random_proj_vectors[i][j].extend(vector_hat)
        self.random_proj_vectors = np.asarray(self.random_proj_vectors)
        yu = 0.0
        for i in range(n):
            for j in range(l):
                key = ""
                for f in range(k):
                    #val = (np.dot(self.random_proj_vectors[j][f], self._data[i]))
                    #yu+=abs(val)
                    #print(val)
                    key+=("," + (str(math.floor((np.dot(self.random_proj_vectors[j][f], self._data[i]) + self.shifts[j][f]) / self.w))))
                print("hash=",key)
                if key not in self.dict_arr[j]:
                    self.dict_arr[j][key] = []
                self.dict_arr[j][key].append(i)
        print("diameter",yu/(n*l*k))

    def query(self, q):
        index_res = []
        for j in range(self.layers):
            key = ""
            for f in range(self.k):
                key+=("," + (str(math.floor((np.dot(self.random_proj_vectors[j][f], q) + self.shifts[j][f]) / self.w))))
            print("all data in single layer unique layer", j ,self.dict_arr[j][key])
            index_res.extend(self.dict_arr[j][key])
        return index_res






