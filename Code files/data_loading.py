from pymongo import MongoClient
import collections
import csv
import xml.etree.ElementTree as ET
import os
from scipy import sparse
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
from operator import itemgetter
from sklearn.metrics.pairwise import euclidean_distances
from decomposition_algorithms import Decomposition

class DataLoading:

    def drop_database(self):
        client = MongoClient('localhost', 27017) 
        client.drop_database('mwdb')

    def insert_textual_data(self, filename, tablename):
        with open(filename, encoding="utf8") as f:
            lines = f.readlines()
            client = MongoClient('localhost', 27017)
            db = client['mwdb']
            table = db[tablename]
            dataArr = []
            for line in lines:
                words = line.split(' ')
                data = collections.OrderedDict()
                data['id'] = words[0]
                data['desc'] = []

                i = 1;
                while i + 3 < len(words):
                    textDesc = collections.OrderedDict()
                    textDesc['term'] = words[i][1:-1]
                    textDesc['TF'] = words[i + 1]
                    textDesc['DF'] = words[i + 2]
                    textDesc['TF-IDF'] = words[i + 3]
                    data['desc'].append(textDesc)
                    i = i + 4

                dataArr.append(data)

            table.insert_many(dataArr)

    def insert_location_textual_data(self, filename, tablename):
        with open(filename, encoding="utf8") as f:
            lines = f.readlines()
            client = MongoClient('localhost', 27017)
            db = client['mwdb']
            table = db[tablename]
            locations = db['locations']
            dataArr = []
            for line in lines:
                words = line.split(' ')
                data = collections.OrderedDict()
                data['title'] = words[0]

                x = 1
                while x < len(words):
                    if words[x][0] == '"':
                        break
                    data['title'] = data['title'] + '_' + words[x]
                    x = x + 1

                data['id'] = locations.find_one({'title': data['title']})['id']
                data['desc'] = []

                i = x
                while i + 3 < len(words):
                    textDesc = collections.OrderedDict()
                    textDesc['term'] = words[i][1:-1]
                    textDesc['TF'] = words[i + 1]
                    textDesc['DF'] = words[i + 2]
                    textDesc['TF-IDF'] = words[i + 3]
                    data['desc'].append(textDesc)
                    i = i + 4

                dataArr.append(data)

            table.insert_many(dataArr)
    def process_users_textual_data(self):

        #insert usertext
        self.insert_textual_data(self.path+'\desctxt\devset_textTermsPerUser.txt', 'usertext')

    def process_images_textual_data(self):

        #insert imagetext
        self.insert_textual_data(self.path+'\desctxt\devset_textTermsPerImage.txt', 'imagetext')

    def process_locations_textual_data(self):

        #insert loctexts
        self.insert_location_textual_data(self.path+'\desctxt\devset_textTermsPerPOI.txt', 'loctext')

    def process_location_data(self):

        filename = self.path + '\devset_topics.xml'

        root = ET.parse(filename).getroot()

        locations = []

        for topic in root.findall('topic'):
            location = {}
            location['id'] = topic.find('number').text
            location['title'] = topic.find('title').text
            location['latitude'] = topic.find('latitude').text
            location['longitude'] = topic.find('longitude').text
            location['wiki'] = topic.find('wiki').text

            locations.append(location)

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db['locations']

        table.insert_many(locations)


    def process_visual_data(self):

        models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db['locations']

        for l in table.find({}):
            data = []
            for m in models:
                model = {}
                arr = []
                filename = self.path + '\descvis\img\\'+l['title']+' '+m+'.csv'
                with open(filename, encoding="utf8") as f:
                    reader = csv.reader(f, quoting=csv.QUOTE_NONNUMERIC)  # change contents to floats
                    for row in reader:  # each row is a list
                        arr.append(row)

                model['model'] = m
                model['data'] = arr
                data.append(model)
            t = db[l['title']]
            t.insert_many(data)

    def process_common_terms_data(self):

        files = os.listdir(self.path + "\\xml\\")
        data = []
        for file in files:
            root = ET.parse(self.path + "\\xml\\" + file).getroot()
            for photo in root.findall('photo'):
                d = {}
                d['location'] = file[:len(file)-4]
                d['image'] = photo.attrib['id']
                d['user'] = photo.attrib['userid']
                d['imagepath'] = self.path + '\img\\' + file[:len(file)-4] + '\\' + photo.attrib['id'] + '.jpg'
                tags = photo.attrib['tags']
                d['terms'] = len(tags.split(' '))
                data.append(d)

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        table = db['LIU_commonterms']

        table.insert_many(data)

    def generate_img_text_graph(self):
        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        tb = 'imagetext'
        table = db[tb]
        model = 'TF-IDF'

        img_ids = {}
        img_terms = {}

        img_index = 0
        term_index = 0
        for img in table.find({}):
            img_ids[img['id']] = img_index
            img_index = img_index + 1
            for term in img['desc']:
                if term['term'] not in img_terms:
                    img_terms[term['term']] = term_index
                    term_index = term_index + 1


        matrix = sparse.lil_matrix((img_index, term_index), dtype=float)


        for img in table.find({}):
            for term in img['desc']:
                matrix[img_ids[img['id']], img_terms[term['term']]] = term[model]

        cos_sim = cosine_similarity(matrix, matrix)

        table = db['img_img_text']
        for i in range(img_index):
            res = []
            for j in range(img_index):
                res.append({'id': j, 'dist': cos_sim[i][j]})

            sorted(res, key=lambda k: k['dist'], reverse=True)
            table.insert({'id': i, 'data': res})

    def generate_img_img_vis_graph(self):
        print("using visual descriptors")

        client = MongoClient('localhost', 27017)
        db = client['mwdb']
        tb = 'locations'

        table = db[tb]
        models = ['CM', 'CM3x3', 'CN', 'CN3x3', 'CSD', 'GLRLM', 'GLRLM3x3', 'HOG', 'LBP', 'LBP3x3']
        data = []
        #count = 0
        self.locations_img_ids = {}
        #img_dist = {}
        index = 0
        image_ids = []


        for loc in table.find({}):
            index += 1
            images = []
            for idx, model in enumerate(models):
                each_loc_model_table = db[loc['title']].find({"model":model})[0]
                images_with_ids = np.array(each_loc_model_table['data'])
                #images_with_ids = images_with_ids.astype(np.float)
                if idx == 0:
                    image_ids.extend(images_with_ids[:, 0])
                    images.extend(images_with_ids[:, 1:])
                else:
                    images = np.concatenate((images, images_with_ids[:, 1:]), axis=1)
            data.extend(images)

        data = np.asarray(data)
        pca = Decomposition(data, 400, 'PCA', [], scale=True)
        euc_distances = euclidean_distances(pca.decomposed_data, pca.decomposed_data)
        euc_distances = np.asarray(euc_distances)

        img_img_tb = 'image_image_vis'
        img_id_tb = 'image_id_vis'

        for i in range(len(euc_distances)):
            distances = []
            for j in range(len(euc_distances)):
                distances.append({'id': j, 'dist': euc_distances[i][j]})
            distances.sort(key=lambda k: k['dist'])
            #db[img_img_tb].insert({'id': i, 'data': [{'id': d['id']} for d in distances]})
            db[img_img_tb].insert({'data': [d['id'] for d in distances]})
            db[img_id_tb].insert({'id': i, 'image_id': image_ids[i]})

    def __init__(self, p):

        self.path = p

