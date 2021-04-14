import unittest
from agent import fd_table

class MyTestCase(unittest.TestCase):

    # 正常初始化socket判断
    def test1(self):
        fd_table = Fd_table()
        self.assertEqual(True, False)


if __name__ == '__main__':
    unittest.main()
