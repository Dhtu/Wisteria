#!/usr/bin/python

import os, stat


def is_sock(pid, fd):
    path = "/proc/34/fd/5"

    info = os.stat(path)

    if stat.S_ISSOCK(info.st_mode):
        print("it is a socket fd")

    elif stat.S_ISLNK(info.st_mode):
        print("it is a link")

    else:
        print("i dont know")

is_sock(0,0)