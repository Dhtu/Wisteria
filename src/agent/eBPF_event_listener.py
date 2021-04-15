#!/usr/bin/python
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'SuDrang'

import os
import socket

DEBUG = True
KAFKA_SERVER_IP = '172.17.0.1:9092'
if not DEBUG:
    from kafka import KafkaProducer
from fd_table import *
from tps_item import *


class EBPF_event_listener:
    relative_ts = True
    print_message = DEBUG  # 是否在命令行打印

    def __init__(self):
        if not DEBUG:
            self.producer = KafkaProducer(bootstrap_servers=[KAFKA_SERVER_IP])
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.current_pid = os.getpid()
        self.start = 0
        self.fd_table = Fd_table()

    def event_filter(self, event):
        if event.comm != b"bash" \
                and event.comm != b"ls" \
                and event.comm != b"ps" \
                and event.pid != self.current_pid \
                :
            return True
        else:
            return False

    def output(self, topic, message):
        if not DEBUG:
            self.producer.send(topic, key=None, value=message, partition=0)
        if self.print_message:
            print(message)

    def get_ts(self, event_ts):
        if self.start == 0:
            self.start = event_ts
        if self.relative_ts:
            return (float(event_ts) - self.start) / 1000000
        else:
            return event_ts

    def on_write(self, event):

        if self.event_filter(event):
            tps_item = Tps_item(event.pid, event.fd, event.ts, False, event.comm)
            is_sock = self.fd_table.is_sock(tps_item)

            event_text = b"%-9.3f" % (self.get_ts(event.ts))
            event_text += b" %-16s %-6d %-6d" % (event.comm, event.pid, event.fd)
            event_text += b" write "
            event_text += b"%-10s" % bytes(self.ip, encoding="utf8")

            self.output('tps', event_text)
            print(is_sock)

    def on_read(self, event):

        if self.event_filter(event):
            tps_item = Tps_item(event.pid, event.fd, event.ts, False, event.comm)
            is_sock = self.fd_table.is_sock(tps_item)

            event_text = b"%-9.3f" % (self.get_ts(event.ts))
            event_text += b" %-16s %-6d %-6d" % (event.comm, event.pid, event.fd)
            event_text += b" read "
            event_text += b"%-10s" % bytes(self.ip, encoding="utf8")

            self.output('tps', event_text)
            print(is_sock)

    def on_socket(self, event):
        if self.event_filter(event):
            event_text = b"%-9.3f" % (self.get_ts(event.ts))
            event_text += b" %-16s %-6d" % (event.comm, event.pid)
            event_text += b"%-10d" % event.fd
            event_text += b" socket "

            self.output('tps', event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, event.ts, True))

    def on_accept(self, event):
        if self.event_filter(event):
            event_text = b"%-9.3f" % (self.get_ts(event.ts))
            event_text += b" %-16s %-6d" % (event.comm, event.pid)
            event_text += b"%-10d" % event.fd
            event_text += b" accept "

            self.output('tps', event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, event.ts, True))

    # todo: close监听了不关心的fd，后续可以优化
    # todo: close不一定正常返回，后续可以监听其exit, 只监听enter出现了多次重复close的情况，不知道是否与此有关
    def on_close(self, event):
        if self.event_filter(event):
            event_text = b"%-9.3f" % (self.get_ts(event.ts))
            event_text += b" %-16s %-6d" % (event.comm, event.pid)
            event_text += b"%-10d" % event.fd
            event_text += b" close "

            self.output('tps', event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, event.ts, False))


ebpf_event_listener = EBPF_event_listener()
