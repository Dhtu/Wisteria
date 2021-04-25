import re
import os


# 对本机已存在的网络进行查找 初始化表
# 返回值有：pid fd is_server
# 数组下标 1：pid
#         3：fd
#         8：ip:port->ip:port
def ip_port_split(str1):
    ip_port = str1.split('->', maxsplit=1)[0].split(':', maxsplit=1)
    if ip_port[0] == '*':
        ip_port[0] = '127.0.0.1'
    return tuple(ip_port)


listen_list = []        # 存储的是pid，fd二元组
establisged_map = {}    # 存储的是{（pid，fd）：（ip，port）}


def init():
    nowTime = os.popen('lsof -i -n -P|grep LISTEN|grep IPv4')
    b = nowTime.readlines()
    for line in b:
        str_list = line.split()
        listen_list.append(ip_port_split(str_list[8]))

    nowTime = os.popen('lsof -i -n -P|grep ESTABLISHED|grep IPv4')
    b = nowTime.readlines()
    for line in b:
        str_list = line.split()
        establisged_map[(str_list[1], re.search(r'\d', str_list[3]).group())] = ip_port_split(str_list[8])
    for key, value in establisged_map.items():
        if listen_list.count(value) >= 1:
            is_server = 1
        else:
            is_server = 0
        print('pid = ' + str(key[0]) + '    fd =' + str(key[1]) + '   isServer = ' + str(is_server))


init()
