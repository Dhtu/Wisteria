#!/usr/bin/python
from kafka import KafkaConsumer

consumer = KafkaConsumer('quickstart-events', bootstrap_servers= ['localhost:9092'])
for msg in consumer:
    print(msg)
