#!/usr/bin/python
from kafka import KafkaConsumer
import sys

from tps_unit import *

consumer = KafkaConsumer('tps', bootstrap_servers=['172.17.0.1:9092'])


def msg_processor(b, count_dict):
    s = str(b, encoding="utf-8").split()

    if s[5] not in count_dict:
        count_dict[s[5]] = 0

    count_dict[s[5]] += 1

    print("%-10s %-6d %-6s %-6s %-6s " % (s[5], count_dict[s[5]], s[2], s[3], s[4]))


tt = tps_table()

count_dict = dict()

while True:
    try:
        for msg in consumer:
            msg_processor(msg.value, count_dict)
    except KeyboardInterrupt:
        exit()
