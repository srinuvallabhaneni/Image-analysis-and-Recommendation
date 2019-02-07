import numpy as np
from pymongo import MongoClient
from sklearn import metrics
from sorted_list import sorted_list
import UI.HTMLPicGallery as PA
from page_rank_algorithms import PageRanks

import pandas as pd
class Phase3_Task_6b:

    def task6b(self, data, fileName):
        labelled_data = pd.read_csv(fileName, delim_whitespace=True)
        labelled_data = labelled_data.drop(0)
        labelled_dict = {}
        for index, row in labelled_data.iterrows():
            if row['label'] not in labelled_dict:
                labelled_dict[row['label']] = [row['image']]
            else:
                labelled_dict[row['label']].append(row['image'])

        pagelables = []
        pageranks = []
        for key in labelled_dict:
            pr = PageRanks()
            ranks = pr.personalized_page_rank(data, labelled_dict[key], False)
            pageranks.append(ranks)
            pagelables.append(key)

        pic_info = []
        for i in range(len(data.img_ids)):
            max = 0
            lables = []
            for j in range(len(pagelables)):
                if pageranks[j][i] > max:
                    lables = [pagelables[j]]
                    max = pageranks[j][i]
                elif pageranks[j][i] == max:
                    lables.append(pagelables[j])
            pic_info.append({'id': str(data.img_ids[i]), 'info': str(data.img_ids[i])+" : "+",".join(lables)})

        PA.display_images(pic_info, 'Task 6b - '+str(fileName))



