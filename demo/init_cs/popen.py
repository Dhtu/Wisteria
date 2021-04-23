# 对本机已存在的网络进行查找 初始化表
# 返回值有：pid fd is_server
import os
# 数组下标 1：pid
#         3：fd
#         8：ip:port->ip:port

# def test_filter(str):
#     str_list = str.split()
#     print(str_list)

listen_list = []
def init():
    nowTime = os.popen('lsof -i -n -P|grep LISTEN|grep IPv4')
    b = nowTime.readlines()
    for line in nowTime:
        str_list = str.split()
        

    # nowTime = os.popen('lsof -i -n -P|grep LISTEN')



# #!/usr/bin/env python
# # -*- coding: utf-8 -*-
# Python IP地址和端口的分割方法
# import re
# import urllib.parse
# from typing import Tuple, Optional
#
# # . 一次或多次,()结果整体为一个分组
# _netloc_re = re.compile(r"^(.+):(\d+)$")
#
#
# def split_host_and_port(input_url: str) -> Tuple[str, Optional[int]]:
#     """
#         取出IP地址和端口 返回：`(host, port)` 元组
#     """
#     parsed_ret = urllib.parse.urlsplit(input_url)
#     if parsed_ret.scheme not in ("http", "https"):
#         raise ValueError("Unsupported url scheme: %s" % input_url)
#     netloc = parsed_ret.netloc
#     match = _netloc_re.match(netloc)
#     if match:
#         host = match.group(1)
#         port = int(match.group(2))  # type: Optional[int]
#     else:
#         host = netloc
#         if parsed_ret.scheme == 'http':
#             port = 80
#         elif parsed_ret.scheme == 'https':
#             port = 443
#         else:
#             port = None
#     return (host, port)
#
# if __name__ == '__main__':
#     ret = split_host_and_port('https://www.cnblogs.com/liown/p/9927879.html')
#     print(ret)  # ('www.cnblogs.com', 443)