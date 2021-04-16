#!/usr/bin/python
from kafka import KafkaConsumer
import sys

from tps_unit import *


consumer = KafkaConsumer('tps', bootstrap_servers=['172.17.0.1:9092'])


def msg_processor(b, tt):
    s = str(b, encoding="utf-8").split()
    ti = tps_item(s[0], s[2], s[3], s[4])
    tt.add_item(ti)

    # for debug
    if tt.get_tps('172.17.0.2') != 0:
        print(tt.get_tps('172.17.0.2'))
        print(tt.get_delay('172.17.0.2'))


tt = tps_table()

while True:
    try:
        for msg in consumer:
            # print_byte(msg.value)
            msg_processor(msg.value, tt)
    except KeyboardInterrupt:
        exit()
