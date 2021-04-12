#!/usr/bin/python
# -*- coding: utf-8 -*-

' a test module '

__author__ = 'SuDrang'

import socket
import os
from kafka import KafkaProducer


class EBPF_event_listener:
    relative_ts = True
    print_message = False

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=['172.17.0.1:9092'])
        self.hostname = socket.gethostname()
        self.ip = socket.gethostbyname(self.hostname)
        self.current_pid = os.getpid()
        self.start = 0

    def event_filter(self, event):
        if event.pid != self.current_pid \
                and event.comm != b"bash" \
                :
            return True
        else:
            return False

    def send_to_kafka(self, topic, message):
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
            event_text = b"%-9.3f" % (self.get_ts(event.ts))
            event_text += b" %-16s %-6d %-6d" % (event.comm, event.pid, event.fd)
            event_text += b" write "
            event_text += b"%-10s" % bytes(self.ip, encoding="utf8")

            self.send_to_kafka('tps', event_text)

    def on_read(self, event):
        if self.event_filter(event):
            event_text = b"%-9.3f" % (self.get_ts(event.ts))
            event_text += b" %-16s %-6d %-6d" % (event.comm, event.pid, event.fd)
            event_text += b" read "
            event_text += b"%-10s" % bytes(self.ip, encoding="utf8")

            self.send_to_kafka('tps', event_text)


ebpf_event_listener = EBPF_event_listener()
