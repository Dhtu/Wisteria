#!/usr/bin/python
# -*- coding: utf-8 -*-

""" a test module """

__author__ = 'SuDrang'

import socket
from matching_rw import *

DEBUG = True
KAFKA_SERVER_IP = '172.17.0.1:9092'
if not DEBUG:
    from kafka import KafkaProducer
from fd_table import *


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
        self.cs_matcher = matching_rw()
        self.system_call_table = {
            0: self.on_read,
            1: self.on_write,
            2: self.on_socket,
            3: self.on_close,
            4: self.on_accept,
            5: self.on_connect,
            6: self.on_fork
        }

    def routing(self, event):
        recall = self.system_call_table[event.sys_call_id]
        if recall:
            recall(event)

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
    def debug_format(enter_ts, exit_ts, comm, pid, fd, message):
        event_text = b"%-9.3f %-9.3f " % (enter_ts, exit_ts)
        event_text += b" %-16s %-10d %-10d" % (comm, pid, fd)
        event_text += message
        return event_text

    @staticmethod
    def output(message):
        print(message)

    def output2kafka(self, topic, message):
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

            enter_ts = self.get_ts(event.enter_ts)
            exit_ts = self.get_ts(event.exit_ts)

            is_sock = self.fd_table.is_sock(event.pid, event.fd, enter_ts)

            event_text = self.debug_format(enter_ts, exit_ts, event.comm,
                                           event.pid, event.fd, b"write")
            if is_sock:
                event_text += b' is sock'
                is_server = self.fd_table.get_cs(event.pid, event.fd)
                message = self.cs_matcher.matching_rw(event.pid, event.fd, enter_ts, exit_ts, is_server, False)
                self.output2kafka(message)
                if is_server:
                    event_text += b' is server'
                else:
                    event_text += b' is client'

                self.output(event_text)
            else:
                event_text += b' is not sock'

            # self.output('tps', event_text)

    def on_read(self, event):

        if self.event_filter(event):
            enter_ts = self.get_ts(event.enter_ts)
            exit_ts = self.get_ts(event.exit_ts)
            is_sock = self.fd_table.is_sock(event.pid, event.fd, enter_ts)

            event_text = self.debug_format(enter_ts, exit_ts, event.comm,
                                           event.pid, event.fd, b"read")
            if is_sock:
                event_text += b' is sock'
                is_server = self.fd_table.get_cs(event.pid, event.fd)

                message = self.cs_matcher.matching_rw(event.pid, event.fd, enter_ts, exit_ts, is_server, True)
                self.output2kafka(message)
                if is_server:
                    event_text += b' is server'
                else:
                    event_text += b' is client'

                self.output(event_text)
            else:
                event_text += b' is not sock'

            # self.output('tps', event_text)

    def on_socket(self, event):
        if self.event_filter(event):
            enter_ts = self.get_ts(event.enter_ts)
            exit_ts = self.get_ts(event.exit_ts)

            event_text = self.debug_format(enter_ts, exit_ts, event.comm,
                                           event.pid, event.fd, b"socket")
            self.output(event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, self.get_ts(event.exit_ts), True))

    def on_accept(self, event):
        if self.event_filter(event):
            enter_ts = self.get_ts(event.enter_ts)
            exit_ts = self.get_ts(event.exit_ts)

            event_text = self.debug_format(enter_ts, exit_ts, event.comm,
                                           event.pid, event.fd, b"accept")

            self.output(event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, self.get_ts(event.exit_ts), True))

            self.fd_table.set_cs(event.pid, event.fd, True)

    def on_close(self, event):
        if self.event_filter(event):
            enter_ts = self.get_ts(event.enter_ts)
            exit_ts = self.get_ts(event.exit_ts)

            event_text = self.debug_format(enter_ts, exit_ts, event.comm,
                                           event.pid, event.fd, b"close")

            self.output(event_text)

            self.fd_table.put_item(Sock_fd_item(event.pid, event.fd, self.get_ts(event.exit_ts), False))

            self.cs_matcher.delete(event.pid, event.fd)

    def on_fork(self, event):
        if self.event_filter(event):
            enter_ts = self.get_ts(event.enter_ts)
            exit_ts = self.get_ts(event.exit_ts)

            self.fd_table.map_copy(event.pid, event.fd)
            event_text = self.debug_format(enter_ts, exit_ts, event.comm,
                                           event.pid, event.fd, b"fork")
            self.output(event_text)

    def on_connect(self, event):
        if self.event_filter(event):
            enter_ts = self.get_ts(event.enter_ts)
            exit_ts = self.get_ts(event.exit_ts)

            event_text = self.debug_format(enter_ts, exit_ts, event.comm,
                                           event.pid, event.fd, b"connect")
            self.output(event_text)

            self.fd_table.set_cs(event.pid, event.fd, False)


ebpf_event_listener = EBPF_event_listener()
