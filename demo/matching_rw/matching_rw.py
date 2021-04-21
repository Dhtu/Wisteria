class matching_rw:
    def __init__(self):
        self.dict = {}

    # 初步想法就是pid，fd对应一个list，list里面存储的是对应的时间
    # 例如：server里面存的就是read的开始时间和结束时间，如果下次读取到的是read，就将列表里面的exit（也就是第二个元素）时间更改成实参的exit时间
    # 如果是读取到的write，就进行相应的输出
    # error情况:探针在探入之前就已经建立了连接，此时如果server直接读取的是wirte，而没有对应的链表，这里我们进行丢弃处理，并打印出来错误
    def matching_rw(self, pid, fd, enter_ts, exit_ts, is_server, is_read):
        if is_server == 1:
            if is_read == 1:
                try:
                    self.dict[(pid, fd)][1] = exit_ts
                except KeyError:
                    self.dict[(pid, fd)] = [enter_ts, exit_ts]
            else:
                try:
                    print("read持续时间"+str(self.dict[(pid, fd)][1]-self.dict[(pid, fd)][0])+"exit_read-enter_write时间"+str(enter_ts-self.dict[(pid, fd)][1])+"write持续时间"+str(exit_ts-enter_ts))
                except KeyError:
                    print("服务端先write了")
        else:
            if is_read == 0:
                try:
                    self.dict[(pid, fd)][1] = exit_ts
                except KeyError:
                    self.dict[(pid, fd)] = [enter_ts, exit_ts]
            else:
                try:
                    print("write持续时间"+str(self.dict[(pid, fd)][1]-self.dict[(pid, fd)][0])+"exit_write-enter_read时间"+str(enter_ts-self.dict[(pid, fd)][1])+"read持续时间"+str(exit_ts-enter_ts))
                except KeyError:
                    print("客户端先read了")

t = matching_rw()
t.matching_rw(1,1,2.5,3.5,1,1)
t.matching_rw(2,2,2.5,3.5,0,0)
t.matching_rw(1,1,3.7,4.5,1,0)
t.matching_rw(2,2,3.7,4.5,0,1)