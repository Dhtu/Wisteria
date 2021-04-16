#!/usr/bin/python
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'SuDrang'

class Tps_item:
    def __init__(self,pid,fd,ts,read_flag,comm):
        self.pid = pid
        self.fd = fd
        self.ts = ts
        self.read_flag = read_flag
        self.comm = comm
