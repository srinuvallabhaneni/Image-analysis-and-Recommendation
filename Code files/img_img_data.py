from scipy import sparse
import numpy as np

class Img_Img_Data:

    def print_graph(self, ids, graph, k):
        file = open("img_img_graph.txt", "w")
        for index, g in enumerate(graph):
            image_id = ids[index]
            file.write(str(image_id) + " = {")
            for img in g:
                id = ids[img]
                file.write(str(id) + "; ")
            file.write(" }\n")
            # if index > 0:
            #     break
        file.close()
        print("Graph written to file  - img_img_graph.txt. Please open to see the graph")

    def __init__(self,ids, g, k):
        self.img_ids = ids
        self.graph = g
        self.k = k
        n = len(ids)
        self.adjacency_mat = sparse.lil_matrix((n, n), dtype=float)
        self.degree_mat = np.zeros(n)
        for i in range(n):
            for j in range(k):
                x = g[i][j]
                self.adjacency_mat[i, x] = 1
                self.degree_mat[x] = self.degree_mat[x] + 1

        self.print_graph(ids, g, k)