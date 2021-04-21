#!/usr/bin/python
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'SuDrang'

class Tps_item:
    def __init__(self, pid, fd, enter_ts,exit_ts, read_flag, comm):
        self.pid = pid
        self.fd = fd
        self.ts = enter_ts
        self.exit_ts = exit_ts
        self.read_flag = read_flag
        self.comm = comm
