class matching_rw:
    def __init__(self):
        self.map = {}

    # 初步想法就是pid，fd对应一个list，list里面存储的是对应的时间和上一次调用的函数和三次对应的时间[enter_ts,exit_ts,read_flag,ts1,ts2,ts3]
    # 例如：server里面存的就是read的开始时间和结束时间，如果下次读取到的是read，就将列表里面的exit（也就是第二个元素）时间更改成实参的exit时间
    # 如果是读取到的write，就进行相应的输出
    # error情况:探针在探入之前就已经建立了连接，此时如果server直接读取的是wirte，而没有对应的链表，这里我们进行丢弃处理，并打印出来错误
    def matching_rw(self, pid, fd, enter_ts, exit_ts, is_server, is_read):

        if is_server == 1:
            try:
                if is_read == 1 and self.map[(pid, fd)][2] == -1:  # -1,r
                    try:
                        self.map[(pid, fd)][0] = enter_ts
                        self.map[(pid, fd)][1] = exit_ts
                        self.map[(pid, fd)][2] = is_read
                    except KeyError:
                        self.map[(pid, fd)] = [enter_ts, exit_ts, is_read, -1, -1, -1]
                elif is_read == 1 and self.map[(pid, fd)][2] == 1:  # r r
                    try:
                        self.map[(pid, fd)][1] = exit_ts
                        self.map[(pid, fd)][2] = is_read
                    except KeyError:
                        self.map[(pid, fd)] = [enter_ts, exit_ts, is_read, -1, -1, -1]
                elif self.map[(pid, fd)][2] == 1 and is_read == 0:  # r w
                    try:
                        self.map[(pid, fd)][3] = self.map[(pid, fd)][1] - self.map[(pid, fd)][0]
                        self.map[(pid, fd)][4] = enter_ts - self.map[(pid, fd)][1]
                        self.map[(pid, fd)][0] = enter_ts
                        self.map[(pid, fd)][1] = exit_ts
                        self.map[(pid, fd)][2] = is_read
                    except KeyError:
                        self.map[(pid, fd)] = [enter_ts, exit_ts, is_read, -1, -1, -1]
                elif self.map[(pid, fd)][2] == 0 and is_read == 0:  # w w
                    try:
                        self.map[(pid, fd)][1] = exit_ts
                    except KeyError:
                        self.map[(pid, fd)] = [enter_ts, exit_ts, is_read, -1, -1, -1]
                elif self.map[(pid, fd)][2] == 0 and is_read == 1:  # w r
                    try:
                        self.map[(pid, fd)][5] = self.map[(pid, fd)][1] - self.map[(pid, fd)][0]
                        print(pid, fd, "ts1", self.map[(pid, fd)][3])
                        print(pid, fd, "ts2", self.map[(pid, fd)][4])
                        print(pid, fd, "ts3", self.map[(pid, fd)][5])
                        self.map[(pid, fd)] = [enter_ts, exit_ts, is_read, -1, -1, -1]
                    except KeyError:
                        self.map[(pid, fd)] = [enter_ts, exit_ts, is_read, -1, -1, -1]
                else:  # -1 w 出错了
                    print("出错了，服务器先write了或者客户端先read了")
            except KeyError:
                self.map[(pid, fd)] = [enter_ts, exit_ts, is_read, -1, -1, -1]
        else:
            if is_read == 1:
                is_read = 0
            else:
                is_read = 1
            is_server = 1
            self.matching_rw(pid, fd, enter_ts, exit_ts, is_server, is_read)

    def delete(self, pid, fd):
        try:
            del self.map[(pid, fd)]
        except KeyError:
            print("此pid fd 不存在")


# t = matching_rw()
#  (pid, fd, enter_ts, exit_ts, is_server, is_read)
# server r r r w w w r r w w r
# t.matching_rw(1, 1, 2, 3, 1, 1)
# t.matching_rw(1, 1, 4, 5, 1, 1)
# t.matching_rw(1, 1, 6, 7, 1, 1)
# t.matching_rw(1, 1, 8, 9, 1, 0)
# t.matching_rw(1, 1, 10, 11, 1, 0)
# t.matching_rw(1, 1, 12, 13, 1, 0)
# t.matching_rw(1, 1, 14, 15, 1, 1)
# t.matching_rw(1, 1, 16, 17, 1, 1)
# t.matching_rw(1, 1, 18, 19, 1, 0)
# t.matching_rw(1, 1, 20, 21, 1, 0)
# t.matching_rw(1, 1, 22, 23, 1, 1)
#
# # client r r r w w w r r w w r
# t.matching_rw(1, 1, 2, 3, 0, 0)
# t.matching_rw(1, 1, 4, 5, 0, 0)
# t.matching_rw(1, 1, 6, 7, 0, 0)
# t.matching_rw(1, 1, 8, 9, 0, 1)
# t.matching_rw(1, 1, 10, 11, 0, 1)
# t.matching_rw(1, 1, 12, 13, 0, 1)
# t.matching_rw(1, 1, 14, 15, 0, 0)
# t.matching_rw(1, 1, 16, 17, 0, 0)
# t.matching_rw(1, 1, 18, 19, 0, 1)
# t.matching_rw(1, 1, 20, 21, 0, 1)
# t.matching_rw(1, 1, 22, 23, 0, 0)
# t.delete(1, 1)
