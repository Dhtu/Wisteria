import os

nowTime = os.popen('lsof -i|grep TCP')
b = nowTime.readlines(10)
for line in nowTime:
    print("我换行了")
    print(line)
# print(nowTime.read())
