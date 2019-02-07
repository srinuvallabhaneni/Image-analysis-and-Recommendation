from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.decomposition import TruncatedSVD
from sklearn.decomposition import LatentDirichletAllocation
from scipy import sparse
from scipy.sparse import linalg
import pandas as pd
import numpy as np


class Decomposition:

    def __init__(self, data, k, algorithm, features, scale=False):
        _data = np.array(data)
        if scale:
            _data = StandardScaler().fit_transform(data)
        if algorithm == 'PCA':
            model = PCA(n_components=k, svd_solver='arpack')
        elif algorithm == 'SVD':
            model = TruncatedSVD(n_components=k, algorithm='arpack')
        elif algorithm == 'LDA':
            model = LatentDirichletAllocation(n_components=k)
        else:
            raise Exception('Unrecognized algorithm '+algorithm)

        self.decomposed_data = model.fit_transform(_data)
        print(sum(model.explained_variance_ratio_[:400]))
        self.loading_scores = []
        for i in range(0, k):
            if algorithm != 'LDA':
                scores = model.explained_variance_ratio_[i] * np.absolute(model.components_[i])
            else:
                scores = model.components_[i]
            if len(features) == 0:
                l_s = pd.Series(scores)
            else:
                l_s = pd.Series(scores, index=features)
            self.loading_scores.append(pd.Series.sort_values(l_s, ascending=False))

class Decomposition_Sparse:

    def sparse_cov(self, A):

        A = A.astype(np.float16)
        n = A.shape[1]

        # Compute the covariance matrix
        rowsum = A.sum(1)
        centering = rowsum.dot(rowsum.T.conjugate()) / n
        C = (A.dot(A.T.conjugate()) - centering) / (n - 1)

        return C

    def pca_code(self, data, k):
        cov_mat = self.sparse_cov(data.T)
        csr_mat = sparse.csr_matrix(cov_mat)
        evals, evecs = linalg.eigs(csr_mat, k)
        self.variance = evals
        self.components = evecs.T
        m_w = data.dot(evecs)
        return m_w.real

    def __init__(self, data, k, algorithm, features):
        _data = sparse.csr_matrix(data)
        if algorithm == 'PCA':
            self.decomposed_data = self.pca_code(_data, k)
        elif algorithm == 'SVD':
            model = TruncatedSVD(n_components=k, algorithm='arpack')
            self.decomposed_data = model.fit_transform(_data)
            self.variance = model.explained_variance_ratio_
            self.components = model.components_
        elif algorithm == 'LDA':
            model = LatentDirichletAllocation(n_components=k)
            self.decomposed_data = model.fit_transform(_data)
            self.components = model.components_
        else:
            raise Exception('Unrecognized algorithm '+algorithm)

        self.loading_scores = []
        for i in range(0, k):
            if algorithm == 'SVD':
                scores = self.variance[i] * np.absolute(self.components[i])
            elif algorithm == 'PCA':
                scores = (self.variance[i] * np.absolute(self.components[i])).real
            else:
                scores = model.components_[i]
            if len(features) == 0:
                l_s = pd.Series(scores)
            else:
                l_s = pd.Series(scores, index=features)

            self.loading_scores.append(pd.Series.sort_values(l_s, ascending=False))



