# -*- coding:utf-8 -*-

class CircleQueue:

    def __init__(self,maxSize):
        self.head = 0
        self.tail = 0
        self.cnt  = 0
        self.list =[0]*maxSize
        self.size = maxSize

    def is_full(self):
        return self.cnt == self.size

    def is_empty(self):
        return 0 == self.cnt

    def initqueue(self):

        self.head = 0
        self.tail = 0
        self.cnt = 0

    def add(self,element):

        if self.is_full():
            print('insert_data: %s' % element, 'pos:%d' % self.tail, 'cnt :%d' % self.cnt)
            self.list[self.tail] = element
            self.tail = (self.tail + 1) % self.size

        else:
            self.list[self.tail] = element
            self.cnt += 1
            self.tail = (self.tail + 1) % self.size
            print('insert_data: %s' % element, 'pos:%d' % self.tail, 'cnt :%d' % self.cnt)

    def delete(self):

        var_list = []

        if self.is_empty():
            raise Exception('queue is empty')

        if self.is_full():
            raise Exception('queue is empty')


        var_list.append(self.list[self.head])

        self.cnt -= 1
        self.head = (self.head + 1) % self.size

        return var_list


queue = CircleQueue(7)
# for i in range(9):
queue.add(str(13213.42132312))
queue.add(str(23213.42132312))
queue.add(str(33213.42132312))
queue.add(str(43213.42132312))
queue.add(str(123153213.42132312))
queue.add(str(63213.42132312))
queue.add(str(11173213.42132312))
queue.add(str(83213.42132312))
queue.add(str(93213.42132312))

print(queue.list)
