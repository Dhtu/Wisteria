#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 判断FD是否是socket类型的 """

__author__ = 'SuDrang'

import queue


# def on socket(events):
#     sock_fd_item = Sock_fd_item(1,2,200,True)
#
# def on_close(events):
#     sock_fd_item = Sock_fd_item(1, 2, 200, False)
class Sock_fd_item:
    def __init__(self, pid, fd, ts, sock_flag):
        self.pid = pid
        self.fd = fd
        self.ts = ts
        self.sock_flag = sock_flag


class Fd_table_value_item:
    def __init__(self, ts, sock_flag):
        self.ts = ts
        self.sock_flag = sock_flag


class Fd_table_value:
    def __init__(self, maxsize):
        self.q = queue.Queue()
        self.maxsize = maxsize

    def put(self, ts, sock_flag):

        # 如果队列满了就get出一个元素，以增加后续查找效率
        if self.q.qsize() >= self.maxsize:
            self.q.get_nowait()
        self.q.put(Fd_table_value_item(ts, sock_flag))

    @staticmethod
    def is_sock_interval(ts, l_item, r_item):

        # 未在区间内
        if not (l_item.ts < ts < r_item.ts):
            return False

        # 区间左边界不是socket
        if not l_item.sock_flag:
            return False

        return True

    def is_sock(self, ts):
        l = list(self.q.queue)
        size = len(l)

        # 只有一个值（一般是初始化的值）
        if size == 1:

            # 左边界是socket
            if l[0].sock_flag and l[0].ts < ts:
                return True
            else:
                return False
        else:
            for item_pair in [l[i:i + 2] for i in range(size - 1)]:

                # 找到对应区间，左边界是socket
                if self.is_sock_interval(ts, item_pair[0], item_pair[1]):
                    return True

            # 未找到对应边界
            # 最后一次记录是socket
            if l[size-1].sock_flag and l[size-1].ts < ts:
                return True
            else:
                return False


class Fd_table:
    def __init__(self,queue_maxsize=6):
        self.m_table = dict()
        self.queue_maxsize = queue_maxsize

    def put(self, sock_fd_item):
        key = (sock_fd_item.pid, sock_fd_item.fd)

        # 如果是第一次操作这一进程的fd，则初始化value queue
        if key not in self.m_table:
            self.m_table[key] = Fd_table_value(self.queue_maxsize)

        self.m_table[key].put(sock_fd_item.ts, sock_fd_item.sock_flag)

    def is_sock(self, tps_item):
        key = (tps_item.pid, tps_item.fd)

        if key in self.m_table:
            return self.m_table[key].is_sock(tps_item.ts)
        else:
            return False
