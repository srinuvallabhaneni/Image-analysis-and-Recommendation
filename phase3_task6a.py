import numpy as np
from pymongo import MongoClient
from sklearn import metrics
from sorted_list import sorted_list
import UI.HTMLPicGallery as PA
from decomposition_algorithms import Decomposition
from classification_algorithms import WeightedKNN
from classification_algorithms import KNN

import pandas as pd
class Phase3_Task_6a:
    def process_distances(self, labelled_dict, k=None):
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        locations_table = db["locations"].find({})
        data = []
        data_ids = []
        for loc in locations_table:
            images = []
            image_ids = []
            for idx, model in enumerate(models):
                # model = 'CN'
                # idx = 0
                each_loc_model_table = db[loc['title']].find({"model": model})[0]
                images_with_ids = np.array(each_loc_model_table['data'])
                images_with_ids = images_with_ids.astype(np.float)
                if idx == 0:
                    image_ids.extend(images_with_ids[:, 0])
                    images.extend(images_with_ids[:, 1:])
                else:
                    images = np.concatenate((images, images_with_ids[:, 1:]), axis=1)
            data_ids.extend(image_ids)
            data.extend(images)
        self.data_ids = data_ids
        self.data = np.asarray(data)
        decomposition = Decomposition(self.data, 400, 'PCA', [], True)
        self.data = decomposition.decomposed_data
        min = np.amin(self.data)
        self.data+=min
        # split data into rest of images "test data" and "training data"
        # do a weighted knn classifier on it
        # X is data and Y is labels
        cluster_dict = {}
        X_train_ids = []
        X_train = []
        Y_train = []
        X_test_ids = []
        X_test = []
        X_test_ids = []
        for index, id in enumerate(self.data_ids):
            if id in labelled_dict:
                X_train_ids.append(id)
                X_train.append(self.data[index,:])
                Y_train.append(labelled_dict[id])
            else:
                X_test.append(self.data[index,:])
                X_test_ids.append(id)
        X_train = np.asarray(X_train)
        X_test = np.asarray(X_test)
        if k==None:
            knn = WeightedKNN()
        else:
            knn = KNN()
        knn.train_model(X_train, Y_train)
        for index, row in enumerate(X_test):
            assigned_class = knn.classify_me(row) if k==None else knn.classify_me(row, k)
            img_list = cluster_dict.get(assigned_class,[])
            img_list.append(X_test_ids[index])
            cluster_dict[assigned_class] = img_list
        self.cluster_dict = cluster_dict


    def task6a(self, fileName, k=None):
        labelled_data = pd.read_csv(fileName, delim_whitespace=True)
        labelled_data = labelled_data.drop(0)
        labelled_dict = {}
        for index, row in labelled_data.iterrows():
            labelled_dict[float(row['image'])] = row['label']
        self.process_distances(labelled_dict)
        total = 0
        for key in self.cluster_dict:
            pic_info = [{'id': str(int(id)), 'info': str(int(id))+"  "+key} for id in self.cluster_dict[key]]
            PA.display_images(pic_info, 'Task 6a - '+str(fileName))
            #print(pic_info)
            print("cluster name=", key)
            print("images in this cluster= ", self.cluster_dict[key])
            print("size of cluster= ", len(self.cluster_dict[key]))
            total+=len(self.cluster_dict[key])
        print("total=", total)



