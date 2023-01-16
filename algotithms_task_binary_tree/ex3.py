class LimitedBinHeap:
    def __init__(self, limit):
        self.heapList = [0]
        self.currentSize = 0
        self.limit = limit

    def percUp(self, i):
        while i // 2 > 0:
            if self.heapList[i] > self.heapList[i // 2]:
                self.heapList[i // 2], self.heapList[i] = self.heapList[i], self.heapList[i // 2]
            i = i // 2

    def find(self, k):
        if k in self.heapList[1:]:
            return True
        else:
            return False

    def insert(self, k):
        if not self.find(k):
            if self.currentSize < self.limit:
                self.heapList.append(k)
                self.currentSize = self.currentSize + 1
                self.percUp(self.currentSize)
            else:
                imin = self.findMin()
                if self.heapList[imin] < k:
                    self.heapList[imin] = k
                    self.percUp(imin)

    def findMin(self):
        minimum = self.currentSize
        i = 1
        while i * 2 <= self.currentSize:
            a = i * 2
            b = a - 1
            if b > self.currentSize:
                minimum = a
            else:
                if self.heapList[a] < self.heapList[b]:
                    minimum = a
                else:
                    minimum = b
            i = minimum
        return minimum

    def findMax(self):
        return self.heapList[1]

    def maxChild(self, i):
        a = i * 2
        b = a + 1
        if b > self.currentSize:
            return a
        else:
            if self.heapList[a] < self.heapList[b]:
                return a
            else:
                return b

    def percDown(self, i):
        while i * 2 <= self.currentSize:
            mc = self.maxChild(i)
            if self.heapList[i] >= self.heapList[mc]:
                self.heapList[i],  self.heapList[mc] = self.heapList[mc], self.heapList[i]
            i = mc

    def delMax(self):
        retval = self.heapList[1]
        self.heapList[1] = self.heapList[self.currentSize]
        self.currentSize = self.currentSize - 1
        self.heapList.pop()
        self.percDown(1)
        return retval

    def insertList(self, alist: list):
        [self.insert(el) for el in alist]
        return self.heapList

    def buildHeap(self, alist):
        i = len(alist) // 2
        final_list = self.insertList(alist)
        self.currentSize = len(final_list)
        self.heapList = [0] + final_list
        while i > 0:
            self.percDown(i)
            i = i - 1

    def size(self):
        return self.currentSize

    def isEmpty(self):
        return self.currentSize == 0

    def __str__(self):
        return f'{self.heapList[1:]}'
