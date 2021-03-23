#!/usr/bin/python
from kafka import KafkaConsumer
import sys


from tmap import *

consumer = KafkaConsumer('tcpconnect', bootstrap_servers= ['172.17.0.1:9092'])



def msg_processor(b,tm):
    s = str(b, encoding="utf-8").split()
    if s[4] != "127.0.0.1":
        ce = connect_edge(s[4],s[5],s[6])
        tm.add(ce)

        # for debug
        print(s[4] + '\t' + s[5] + '\t' + s[6])


g_tm = topology_map()
while True:
    try:
        for msg in consumer:
            msg_processor(msg.value,g_tm)
    except KeyboardInterrupt:
        exit()
