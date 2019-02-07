from clustering_algorithms import Clustering_Algorithms
import UI.HTMLPicGallery as PA

class Phase3_task2:

    def task_2a(self, data, c):

        c_a = Clustering_Algorithms()
        labels = c_a.spectral_clustering(data, c)
        clusters = [[] for _ in range(c)]

        for i in range(len(labels)):
            clusters[labels[i]].append({'id': data.img_ids[i], 'info': ''})

        for i in range(c):
            print(len(clusters[i]))
            PA.display_images(clusters[i], 'Task 2a - '+str(c))

    def task_2b(self, data, c):

        c_a = Clustering_Algorithms()
        clusters = c_a.normalised_cut(data, c)

        for i in clusters:
            pic_info = []
            print(len(i))
            for j in i:
                pic_info.append({'id': data.img_ids[j], 'info': ''})
            PA.display_images(pic_info, 'Task 2b - ' + str(c))
