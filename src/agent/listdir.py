import os,stat
#import pandas as pd

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

list = []
def traverseDirByListdir(path):
    path = os.path.expanduser(path)
    for f in os.listdir(path):
        if is_number(f.strip()):
            list.append(f.strip())
            #print path+'/'+f.strip()

traverseDirByListdir("/proc")
#print(list)
list1=[]

for i in list:
    path = "/proc/"+i+"/fd"
    #print(path)
    try:
        for f in os.listdir(path):
            info = os.stat(path+"/"+f)
            #print(info)
            if stat.S_ISSOCK(info.st_mode):
                #print(path+"/"+f+"it is a socket fd")
                #print(i,f)
                list2 = [i,f]
                list1.append(list2)
    except OSError:
        pass
    continue
#print("pid= "+list1.i+"\n"+"fd = "+list1.f)

#for s in list1:#判断是否存入进去了
    #print(s)

















