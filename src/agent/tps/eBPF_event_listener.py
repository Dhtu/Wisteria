#!/usr/bin/python
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'SuDrang'

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

    @staticmethod
    def debug_print(ts, comm, pid, fd, message):
        event_text = b"%-9.3f" % ts
        event_text += b" %-16s %-10d %-10d" % (comm, pid, fd)
        event_text += message
        return event_text

    @staticmethod
    def debug_print2(enter_ts, exit_ts, comm, pid, fd, message):
        event_text = b"%-9.3f %-9.3f " % (enter_ts, exit_ts)
        event_text += b" %-16s %-10d %-10d" % (comm, pid, fd)
        event_text += message
        return event_text

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
            tps_item = Tps_item(event.pid, event.fd, event.enter_ts, False, event.comm)
            is_sock = self.fd_table.is_sock(tps_item)

            event_text = self.debug_print2(self.get_ts(event.enter_ts), self.get_ts(event.exit_ts), event.comm,
                                           event.pid, event.fd, b"write")
            if is_sock:
                event_text += b' is sock'
                # print("read")
                # self.output('tps', event_text)
            else:
                event_text += b' is not sock'
            self.output('tps', event_text)

    def on_read(self, event):

        if self.event_filter(event):
            tps_item = Tps_item(event.pid, event.fd, event.enter_ts, False, event.comm)
            is_sock = self.fd_table.is_sock(tps_item)

            event_text = self.debug_print2(self.get_ts(event.enter_ts), self.get_ts(event.exit_ts), event.comm,
                                           event.pid, event.fd, b"read")
            if is_sock:
                event_text += b' is sock'
                # print("write")

            else:
                event_text += b' is not sock'

            self.output('tps', event_text)

    def on_socket(self, event):
        if self.event_filter(event):
            event_text = self.debug_print(self.get_ts(event.ts), event.comm, event.pid, event.fd, b"socket")

            self.output('tps', event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, event.ts, True))

    def on_accept(self, event):
        if self.event_filter(event):
            event_text = self.debug_print(self.get_ts(event.ts), event.comm, event.pid, event.fd, b"accept")

            self.output('tps', event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, event.ts, True))

    def on_close(self, event):
        if self.event_filter(event):
            event_text = self.debug_print(self.get_ts(event.ts), event.comm, event.pid, event.fd, b"close")

            self.output('tps', event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, event.ts, False))

    def on_fork(self, event):
        if self.event_filter(event):
            self.fd_table.map_copy(event.pid, event.ret)
            event_text = self.debug_print(self.get_ts(event.ts), event.comm, event.pid, event.ret, b"fork")
            self.output('tps', event_text)

    def on_connect(self, event):
        if self.event_filter(event):
            event_text = self.debug_print(self.get_ts(event.ts), event.comm, event.pid, event.fd, b"connect")

            self.output('tps', event_text)

            # self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, event.ts, True))

ebpf_event_listener = EBPF_event_listener()
