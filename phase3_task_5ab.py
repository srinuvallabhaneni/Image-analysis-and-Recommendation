import numpy as np
from lsh_index import LSHIndex
from pymongo import MongoClient
from sklearn import metrics
from sorted_list import sorted_list
import UI.HTMLPicGallery as PA
from decomposition_algorithms import Decomposition

class Phase3_Task_5ab:
    def task5a(self, l, k, data=[]):
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        locations_table = db["locations"].find({})
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
                    # image_ids.extend(each_loc_model_table['data'])
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
        self.data+=abs(min)
        self.lsh_index = LSHIndex(self.data, l, k, 15)

    def task5b(self, id, t):
        given_image_index = self.data_ids.index(float(id))
        res = self.lsh_index.query(self.data[given_image_index])
        print('With repetition Overall considered images= ',len(res))
        res = set(res)
        print('Total unique considered images= ',len(res))
        '''
        for i in res:
            print("index =",i)
            print("data id =",self.data_ids[i])
            print("value =",np.linalg.norm(self.data[i]-self.data[given_image_index]))
        '''

        ''' To Rank them in order '''
        distances = sorted_list(t, 'distance', True)
        for i in res:
            dist = np.linalg.norm(self.data[i]-self.data[given_image_index])
            distances.add({'id': self.data_ids[i], 'distance': dist})

        print('Top 5 similar images and similarity score using LSH')
        print()
        pic_info = []
        print('Image id  -  Distance')
        for i in range(0, t):
            o = distances.extract()
            print(str(int(o['id']))+' - '+str(o['distance']))
            pic_info.append({'id': str(int(o['id'])), 'info': str(int(o['id']))})
        PA.display_images(pic_info, 'Task 5b - '+str(id)+' - '+str(t))


        '''To delete'''
'''        s_mat = [self.data[given_image_index]]
        distances = sorted_list(t, 'distance', True)
        euc_distance = metrics.euclidean_distances(s_mat,self.data)
        # euc_distance = metrics.euclidean_distances([self.images[given_image_index]],self.images)
        for i in range(0, len(self.data_ids)):
            distances.add({'id': self.data_ids[i], 'distance': euc_distance[0][i]})
        print('Top 5 similar images and similarity score for validation purpose')
        print()
        for i in range(0,t):
            o = distances.extract()
            print(str(int(o['id']))+' - '+str(o['distance']))
'''



