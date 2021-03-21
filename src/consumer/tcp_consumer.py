#!/usr/bin/python
from kafka import KafkaConsumer
import sys

def print_byte(s, file=sys.stdout, nl=1):
    """
    printb(s)

    print a bytes object to stdout and flush
    """
    buf = file.buffer if hasattr(file, "buffer") else file

    buf.write(s)
    if nl:
        buf.write(b"\n")
    file.flush()

consumer = KafkaConsumer('quickstart-events', bootstrap_servers= ['localhost:9092'])



def msg_processor(b):
    s = str(b, encoding="utf-8").split()
    if s[4] != "127.0.0.1":
        print(s[4]+'\t'+s[5]+'\t'+s[6])

while True:
    try:
        for msg in consumer:
            # print_byte(msg.value)
            msg_processor(msg.value)
    except KeyboardInterrupt:
        exit()
