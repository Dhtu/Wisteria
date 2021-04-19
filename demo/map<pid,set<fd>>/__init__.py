import copy

fd_map = {}

def map_add(pid,fd):
    if pid in fd_map:
        fd_map[pid].add(fd)
    else:
        fd_map[pid]={fd}

def map_delete(pid,fd):
    try:
        fd_map[pid].remove(fd)
    except KeyError:
        print("pid=",pid,"fd=",fd,"not in map")

def map_copy(pid,ppid): #pid is father,ppid is son
    fd_map[ppid]=copy.deepcopy(fd_map[pid])

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


print(fd_map)