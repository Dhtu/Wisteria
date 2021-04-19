import copy

map = {}

def map_add(pid,fd):
    if pid in map:
        map[pid].add(fd)
    else:
        map[pid]={fd}

def map_delete(pid,fd):
    try:
        map[pid].remove(fd)
    except KeyError:
        print("pid=",pid,"fd=",fd,"not in map")

def map_copy(pid,ppid): #pid is father,ppid is son
    map[ppid]=copy.deepcopy(map[pid])

# test information
map_add(1,2)
map_add(1,3)
map_add(1,3)
map_delete(1,3)
map_delete(1,3)
map_add(1,4)
map_add(1,5)
map_add(2,0)
map_copy(1,5)
map_delete(1,2)


print(map)