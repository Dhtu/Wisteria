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


while True:
    try:
        for msg in consumer:
            print_byte(msg.value)
    except KeyboardInterrupt:
        exit()
