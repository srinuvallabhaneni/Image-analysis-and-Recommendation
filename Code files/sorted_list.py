class sorted_list:

    def add(self, object):

        self.__heap.append(object)
        i = len(self.__heap) - 1
        while i > 0:
            if self.__compare(self.__heap[i-1], self.__heap[i]):
                self.__swap(i-1, i)
                i = i-1
            else:
                break

        if len(self.__heap) > self.__size:
            del self.__heap[-1]

    def extract(self):

        if len(self.__heap) == 0:
            return None

        return self.__heap.pop(0)

    def __compare(self, obj1, obj2):

        if self.__is_min:
            return obj1[self.__key] > obj2[self.__key]
        obj1[self.__key] < obj2[self.__key]

    def __swap(self, i, j):

        t = self.__heap[i]
        self.__heap[i] = self.__heap[j]
        self.__heap[j] = t

    def __init__(self, size, key, is_min=True):

        self.__size = size
        self.__key = key
        self.__is_min = is_min
        self.__heap = []
