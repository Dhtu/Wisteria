#!/usr/bin/python
# -*- coding: utf-8 -*-

""" 判断FD是否是socket类型的 """

__author__ = 'SuDrang'

import queue
import os
import stat
import copy
import re

FD_TABLE_DEBUG = False

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
        self.is_server = False

    def __deepcopy__(self, memodict=None):

        if memodict is None:
            memodict = {}

        value_copy = Fd_table_value(self.maxsize)

        l = list(self.q.queue)

        value_copy.is_server = self.is_server

        for item in l:
            value_copy.put(item.ts,item.sock_flag)

        memodict[self] = value_copy

        return value_copy


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
            if l[size - 1].sock_flag and l[size - 1].ts < ts:
                return True
            else:
                return False


class Fd_table:
    def __init__(self, queue_maxsize=6):
        self.m_table = dict() # fd操作记录表
        self.m_fd_map = {} # pid-fd表
        self.queue_maxsize = queue_maxsize
        self.listdir()
        self.init_cs()
        self.DEBUG = FD_TABLE_DEBUG

    def listdir(self):
        list0 = list()
        path = os.path.expanduser("/proc")
        for f in os.listdir(path):
            if self.is_number(f.strip()):
                list0.append(f.strip())
        # list1 = []

        for i in list0:
            path = "/proc/" + i + "/fd"
            try:
                for f in os.listdir(path):
                    info = os.stat(path + "/" + f)
                    if stat.S_ISSOCK(info.st_mode):
                        self.put(int(i), int(f))
            except OSError:
                pass
            continue

    @staticmethod
    def is_number(s):
        try:
            float(s)
            return True
        except ValueError:
            pass

        try:
            import unicodedata
            unicodedata.numeric(s)
            return True
        except (TypeError, ValueError):
            pass

        return False

    def map_add(self, pid, fd):
        if pid in self.m_fd_map:
            self.m_fd_map[pid].add(fd)
        else:
            self.m_fd_map[pid] = {fd}

    def map_delete(self,pid, fd):
        try:
            self.m_fd_map[pid].remove(fd)
        except KeyError :
            if self.DEBUG:
                print("pid=", pid, "fd=", fd, "not in map")

    def map_copy(self,pid, ppid):  # pid is father,ppid is son
        self.m_fd_map[ppid] = copy.deepcopy(self.m_fd_map[pid])
        for fd in self.m_fd_map[pid] :
            self.m_table[(ppid,fd)] = copy.deepcopy(self.m_table[(pid,fd)])

    @staticmethod
    def ip_port_split(str1):
        ip_port = str1.split('->', maxsplit=1)[0].split(':', maxsplit=1)
        if ip_port[0] == '*':
            ip_port[0] = '127.0.0.1'
        return tuple(ip_port)

    def init_cs(self):
        listen_list = []  # 存储的是pid，fd二元组
        establisged_map = {}  # 存储的是{（pid，fd）：（ip，port）}

        nowTime = os.popen('lsof -i -n -P|grep LISTEN|grep IPv4')
        b = nowTime.readlines()
        for line in b:
            str_list = line.split()
            listen_list.append(self.ip_port_split(str_list[8]))

        nowTime = os.popen('lsof -i -n -P|grep ESTABLISHED|grep IPv4')
        b = nowTime.readlines()
        for line in b:
            str_list = line.split()
            establisged_map[(str_list[1], re.search(r'\d', str_list[3]).group())] = self.ip_port_split(str_list[8])
        for key, value in establisged_map.items():
            if listen_list.count(value) >= 1:
                is_server = True
            else:
                is_server = False
            # print('pid = ' + str(key[0]) + '    fd =' + str(key[1]) + '   isServer = ' + str(is_server))
            self.set_cs(int(key[0]),int(key[1]),is_server)
    # 添加fd操作记录
    def put_item(self, sock_fd_item):
        key = (sock_fd_item.pid, sock_fd_item.fd)

        # 如果是第一次操作这一进程的fd，则初始化value queue
        if key not in self.m_table:
            self.m_table[key] = Fd_table_value(self.queue_maxsize)

        self.m_table[key].put(sock_fd_item.ts, sock_fd_item.sock_flag)

        if sock_fd_item.sock_flag:
            self.map_add(sock_fd_item.pid,sock_fd_item.fd)
        else:
            # self.map_delete(sock_fd_item.pid,sock_fd_item.fd)
            pass # 当close在fork前submit出来时，这里就会删除这一set item，但是这会影响先前的

    # 设置是否是服务器
    def set_cs(self,pid,fd,is_server):
        # print("key: %d, fd: %d" % (pid,fd)+str(is_server))
        key = (pid, fd)

        if key in self.m_table:
            self.m_table[key].is_server = is_server
        #
        # print(self.m_table[(11834,3)].is_server)
        # print(self.m_table[(11835,4)].is_server)

        # else:
        #     pass # todo: 异常处理


    def get_cs(self,pid,fd):

        key = (pid, fd)

        if key in self.m_table:
            return self.m_table[(pid,fd)].is_server
        # else:
        #     pass # todo: 异常处理



    # 初始化table
    def put(self, pid, fd):
        key = (pid, fd)

        self.map_add(pid,fd)

        # 如果是第一次操作这一进程的fd，则初始化value queue
        if key not in self.m_table:
            self.m_table[key] = Fd_table_value(self.queue_maxsize)

        self.m_table[key].put(0, True)

    def is_sock(self, pid,fd,ts):
        key = (pid, fd)

        if key in self.m_table:
            return self.m_table[key].is_sock(ts)
        else:
            return False
