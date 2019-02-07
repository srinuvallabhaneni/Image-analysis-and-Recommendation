from page_rank_algorithms import PageRanks
import UI.HTMLPicGallery as PA

class Phase3_task4:

    def task_4(self, data, k, V):

        pr = PageRanks()
        ranks = pr.personalized_page_rank(data, V)

        result = ranks.nlargest(k)

        pic_info = []

        for idx, val in result.iteritems():
            pic_info.append({'id': idx, 'info': idx + ' :'+str(val)})

        PA.display_images(pic_info, 'Task 4 - '+str(k))
