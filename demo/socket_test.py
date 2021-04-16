import ctypes

libc = ctypes.CDLL(None)
syscall = libc.syscall
syscall(41)