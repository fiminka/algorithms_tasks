import numpy as np
import time
import matplotlib.pyplot as plt
import seaborn as sns


class BinHeap:
    def __init__(self):
        self.heapList = [0]
        self.currentSize = 0

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapList[i] < self.heapList[i // 2]:
                self.heapList[i // 2], self.heapList[i] = self.heapList[i], self.heapList[i // 2]
            i = i // 2

    def insert(self, k):
        self.heapList.append(k)
        self.currentSize = self.currentSize + 1
        self.percUp(self.currentSize)

    def findMin(self):
        return self.heapList[1]

    def percDown(self, i):
        while i * 2 <= self.currentSize:
            mc = self.minChild(i)
            if self.heapList[i] > self.heapList[mc]:
                self.heapList[i],  self.heapList[mc] = self.heapList[mc], self.heapList[i]
            i = mc

    def minChild(self, i):
        if i * 2 + 1 > self.currentSize:
            return i * 2
        else:
            if self.heapList[i*2] < self.heapList[i*2+1]:
                return i * 2
            else:
                return i * 2 + 1

    def delMin(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def buildHeap(self, alist):
        i = len(alist) // 2
        self.currentSize = len(alist)
        self.heapList = [0] + alist[:]
        while i > 0:
            self.percDown(i)
            i = i - 1

    def size(self):
        return self.currentSize

    def isEmpty(self):
        return self.currentSize == 0

    def __str__(self):
        return f'{self.heapList[1:]}'


def sortBinHeap(alist):
    l = list(set(alist))
    list_to_sort = BinHeap()
    list_to_sort.buildHeap(l)
    sorted_list = []
    for i in range(list_to_sort.size()):
        sorted_list.append(list_to_sort.delMin())
    return sorted_list


def time_checker(length, simulations=100):
    list_of_time = []
    for i in range(simulations):
        l = np.random.permutation(length)
        start_time = time.time()
        sortBinHeap(l)
        fin_time = time.time()
        list_of_time.append(fin_time - start_time)
    return np.mean(list_of_time)


def simulation():
    amount_of_elem = []
    limit = 51
    for i in range(1, limit):
        amount_of_elem.append(i * 100)

    i = 1
    average_time = []
    for k in amount_of_elem:
        if i % 5 == 0:
            print(f"Iteration {i}/{limit - 1}")
        average_time.append(time_checker(k))
        i += 1

    poly = np.polyfit(amount_of_elem, average_time, 3)
    poly = np.poly1d(poly)

    sns.set()
    plt.plot(amount_of_elem, average_time, 'o', label='sortBinHeap()')
    plt.plot(amount_of_elem, poly(amount_of_elem), label='Polynomial fitting')
    plt.xlabel('amount of elements')
    plt.ylabel('time')
    plt.title('Time analysis')
    plt.legend()
    plt.show()
