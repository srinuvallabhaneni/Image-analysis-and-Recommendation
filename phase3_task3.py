from page_rank_algorithms import PageRanks
import UI.HTMLPicGallery as PA

class Phase3_task3:

    def task_3(self, data, k):

        pr = PageRanks()
        ranks = pr.page_rank(data)

        result = ranks.nlargest(k)

        pic_info = []

        for idx, val in result.iteritems():
            pic_info.append({'id': idx, 'info': idx + ' :'+str(val)})

        PA.display_images(pic_info, 'Task 3 - '+str(k))
