class matching_rw:
    def __init__(self):
        self.map = {(-1,-1),[-1,-1,-1,-1,-1,-1]}
        self.read_flag = -1
    # 初步想法就是pid，fd对应一个list，list里面存储的是对应的时间和上一次调用的函数和三次对应的时间[enter_ts,exit_ts,read_flag,ts1,ts2,ts3]
    # 例如：server里面存的就是read的开始时间和结束时间，如果下次读取到的是read，就将列表里面的exit（也就是第二个元素）时间更改成实参的exit时间
    # 如果是读取到的write，就进行相应的输出
    # error情况:探针在探入之前就已经建立了连接，此时如果server直接读取的是wirte，而没有对应的链表，这里我们进行丢弃处理，并打印出来错误
    def matching_rw(self, pid, fd, enter_ts, exit_ts, is_server, is_read):

        if is_server == 1:
            if is_read == 1 and self.map[(pid, fd)][2] == -1:       # -1,r
                try:
                    self.map[(pid, fd)][0] = enter_ts
                    self.map[(pid, fd)][1] = exit_ts
                    self.map[(pid, fd)][2] = is_read
                except KeyError:
                    self.map[(pid, fd)] = [enter_ts, exit_ts,is_read]
            elif is_read == 1 and self.read_flag == 1:              # r r
                try:
                    self.map[(pid, fd)][1] = exit_ts
                except KeyError:
                    self.map[(pid, fd)] = [enter_ts, exit_ts, is_read]
            elif is_read == 1 and self.read_flag == 0:              # r w
                try:
                    self.map[(pid, fd)][3] = self.map[(pid, fd)][1] - self.map[(pid, fd)][0]
                    self.map[(pid, fd)][4] = enter_ts - self.map[(pid, fd)][1]
                    self.map[(pid, fd)][0] = enter_ts
                    self.map[(pid, fd)][1] = exit_ts
                    self.map[(pid, fd)][2] = is_read
                except KeyError:
                    self.map[(pid, fd)] = [enter_ts, exit_ts, is_read]
            elif is_read == 1 and self.read_flag == 0:              # w w
                try:
                    self.map[(pid, fd)][1] = exit_ts
                except KeyError:
                    self.map[(pid, fd)] = [enter_ts, exit_ts, is_read]
            elif is_read == 1 and self.read_flag == 0:              # w r
                try:
                    self.map[(pid, fd)][5] = self.map[(pid, fd)][1] - self.map[(pid, fd)][0]
                    print(self.map[(pid, fd)][3])
                    print(self.map[(pid, fd)][4])
                    print(self.map[(pid, fd)][5])
                except KeyError:
                    self.map[(pid, fd)] = [enter_ts, exit_ts, is_read]
            else:                                                   # -1 w 出错了
                print("出错了，服务器先write了")


t = matching_rw()
# t.matching_rw(1, 1, 2.5, 3.5, 1, 1)
# t.matching_rw(1, 1, 3.7, 4.2, 1, 1)
# t.matching_rw(2, 2, 2.5, 3.5, 0, 0)
# t.matching_rw(1, 1, 4.7, 5.3, 1, 0)
# t.matching_rw(2, 2, 3.7, 4.5, 0, 1)

#server r r r w







