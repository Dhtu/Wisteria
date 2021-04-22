import unittest
from agent.tps.fd_table import *

class MyTestCase(unittest.TestCase):

    # 1. 正常初始化socket判断
    def test1(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        ret = m_table.is_sock(12,12,5)
        self.assertEqual(True, ret)

    # 2. 正常初始化非socket判断
    def test2(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, False))
        ret = m_table.is_sock(12,12,5)
        self.assertEqual(False, ret)

    # 3. 正常初始化无该fd
    def test3(self):
        m_table = Fd_table()
        ret = m_table.is_sock(12,12,5)
        self.assertEqual(False, ret)

    # 4.1. 打开socket后关闭该fd，在区间内部
    def test4_1(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        ret = m_table.is_sock(12,12,5)
        self.assertEqual(True, ret)

    # 4.2. 打开socket后关闭该fd，在区间外部
    def test4_2(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        ret = m_table.is_sock(12,12,8)
        self.assertEqual(False, ret)

    # 4.3. 打开socket后关闭该fd，再复用fd作为常规文件，在第二段区间内部
    def test4_3(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 9, False))
        ret = m_table.is_sock(12,12,8)
        self.assertEqual(False, ret)

    # 4.4. 打开socket后关闭该fd，再复用fd作为socket文件，在第二段区间内部
    def test4_4(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        ret = m_table.is_sock(12,12,7)
        self.assertEqual(False, ret)

    # 4.5. 打开socket后关闭该fd，再复用fd作为socket文件，然后关闭，在第三段区间内部
    def test4_5(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        m_table.put_item(Sock_fd_item(12, 12, 10, False))
        ret = m_table.is_sock(12,12,9)
        self.assertEqual(True, ret)

    # 4.6. 打开socket后关闭该fd，再复用fd作为socket文件，在第三段区间右边
    def test4_6(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        ret = m_table.is_sock(12,12,9)
        self.assertEqual(True, ret)

    # 5.1. 测试队列经历多次插入后性能表现, 最后一次为socket
    def test5_1(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        m_table.put_item(Sock_fd_item(12, 12, 10, True))
        m_table.put_item(Sock_fd_item(12, 12, 11, False))
        m_table.put_item(Sock_fd_item(12, 12, 12, True))
        m_table.put_item(Sock_fd_item(12, 12, 13, True))
        m_table.put_item(Sock_fd_item(12, 12, 14, False))
        m_table.put_item(Sock_fd_item(12, 12, 15, True))
        ret = m_table.is_sock(12,12,17)
        self.assertEqual(True, ret)

    # 5.2. 测试队列经历多次插入后性能表现, 最后一次为close
    def test5_2(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        m_table.put_item(Sock_fd_item(12, 12, 10, True))
        m_table.put_item(Sock_fd_item(12, 12, 11, False))
        m_table.put_item(Sock_fd_item(12, 12, 12, True))
        m_table.put_item(Sock_fd_item(12, 12, 13, True))
        m_table.put_item(Sock_fd_item(12, 12, 14, False))
        m_table.put_item(Sock_fd_item(12, 12, 15, False))
        ret = m_table.is_sock(12,12,17)
        self.assertEqual(False, ret)

    # 5.3. 测试队列经历多次插入后性能表现, 最后一区间为socket
    def test5_3(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        m_table.put_item(Sock_fd_item(12, 12, 10, True))
        m_table.put_item(Sock_fd_item(12, 12, 11, False))
        m_table.put_item(Sock_fd_item(12, 12, 12, True))
        m_table.put_item(Sock_fd_item(12, 12, 13, True))
        m_table.put_item(Sock_fd_item(12, 12, 14, True))
        ret = m_table.is_sock(12,12,15)
        self.assertEqual(True, ret)

    # 5.4. 测试队列经历多次插入后性能表现, 最后一区间不为socket
    def test5_4(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        m_table.put_item(Sock_fd_item(12, 12, 10, True))
        m_table.put_item(Sock_fd_item(12, 12, 11, False))
        m_table.put_item(Sock_fd_item(12, 12, 12, True))
        m_table.put_item(Sock_fd_item(12, 12, 13, True))
        m_table.put_item(Sock_fd_item(12, 12, 14, False))
        m_table.put_item(Sock_fd_item(12, 12, 17, False))
        ret = m_table.is_sock(12,12,15)
        self.assertEqual(False, ret)

    # 6.1. fork测试
    def test6_1(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.map_copy(12,13)
        ret = m_table.is_sock(13,12,5)
        self.assertEqual(True, ret)

    # 6.2. 两次fork测试
    def test6_2(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.map_copy(12, 13)
        m_table.put_item(Sock_fd_item(13, 5, 2, True))
        m_table.map_copy(13,14)
        ret = m_table.is_sock(14,5,5)
        self.assertEqual(True, ret)

    # 6.3 复杂fork测试，类似5.2
    def test6_3(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        m_table.put_item(Sock_fd_item(12, 12, 10, True))
        m_table.put_item(Sock_fd_item(12, 12, 11, False))
        m_table.put_item(Sock_fd_item(12, 12, 12, True))
        m_table.put_item(Sock_fd_item(12, 12, 13, True))
        m_table.put_item(Sock_fd_item(12, 12, 14, False))
        m_table.put_item(Sock_fd_item(12, 12, 15, False))
        m_table.map_copy(12, 13)
        ret = m_table.is_sock(13,12,17)
        self.assertEqual(False, ret)

    # 6.4 复杂fork测试，类似5.3
    def test6_4(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        m_table.put_item(Sock_fd_item(12, 12, 10, True))
        m_table.put_item(Sock_fd_item(12, 12, 11, False))
        m_table.put_item(Sock_fd_item(12, 12, 12, True))
        m_table.put_item(Sock_fd_item(12, 12, 13, True))
        m_table.put_item(Sock_fd_item(12, 12, 14, True))
        m_table.map_copy(12, 13)
        ret = m_table.is_sock(13,12,15)
        self.assertEqual(True, ret)

    # 6.5 检查深拷贝
    def test6_5(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, True))
        m_table.put_item(Sock_fd_item(12, 12, 6, False))
        m_table.put_item(Sock_fd_item(12, 12, 8, True))
        m_table.put_item(Sock_fd_item(12, 12, 10, True))
        m_table.put_item(Sock_fd_item(12, 12, 11, False))
        m_table.put_item(Sock_fd_item(12, 12, 12, True))
        m_table.put_item(Sock_fd_item(12, 12, 13, True))
        m_table.map_copy(12, 13)
        m_table.put_item(Sock_fd_item(12, 12, 14, False))
        ret = m_table.is_sock(13,12,15)
        self.assertEqual(True, ret)


    # # 7.1 插入顺序不一致
    # def test7_1(self):
    #     m_table = Fd_table()
    #     m_table.put_item(Sock_fd_item(12, 12, 5, False))
    #     m_table.put_item(Sock_fd_item(12, 12, 0, True))
    #     ret = m_table.is_sock(12,12,15)
    #     self.assertEqual(False, ret)
    #
    # # 7.2 插入顺序不一致
    # def test7_2(self):
    #     m_table = Fd_table()
    #     m_table.put_item(Sock_fd_item(12, 12, 5, True))
    #     m_table.put_item(Sock_fd_item(12, 12, 0, False))
    #     ret = m_table.is_sock(12,12,15)
    #     self.assertEqual(True, ret)
    #
    # # 7.3 插入顺序不一致
    # def test7_3(self):
    #     m_table = Fd_table()
    #     m_table.put_item(Sock_fd_item(12, 12, 5, False))
    #     m_table.put_item(Sock_fd_item(12, 12, 0, True))
    #     m_table.put_item(Sock_fd_item(12, 12, 8, False))
    #     ret = m_table.is_sock(12,12,3)
    #     self.assertEqual(True, ret)

    # 8.1 设置服务器标识符
    def test8_1(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, False))
        m_table.put_item(Sock_fd_item(12, 12, 5, True))
        m_table.put_item(Sock_fd_item(12, 12, 8, False))
        m_table.set_cs(12,12,True)
        is_server = m_table.get_cs(12,12)
        self.assertEqual(True, is_server)

    # 8.2 设置客户端标识符
    def test8_2(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, False))
        m_table.put_item(Sock_fd_item(12, 12, 5, True))
        m_table.put_item(Sock_fd_item(12, 12, 8, False))
        m_table.set_cs(12, 12, False)
        is_server = m_table.get_cs(12, 12)
        self.assertEqual(False, is_server)

    # 8.3 检查fork
    def test8_3(self):
        m_table = Fd_table()
        m_table.put_item(Sock_fd_item(12, 12, 0, False))
        m_table.put_item(Sock_fd_item(12, 12, 5, True))
        m_table.put_item(Sock_fd_item(12, 12, 8, False))
        m_table.set_cs(12, 12, True)
        m_table.map_copy(12, 13)
        is_server = m_table.get_cs(13, 12)
        self.assertEqual(True, is_server)

if __name__ == '__main__':
    unittest.main()
