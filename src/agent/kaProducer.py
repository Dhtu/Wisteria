from kafka import KafkaProducer

producer = KafkaProducer(bootstrap_servers=['localhost:9092'])
future = producer.send('quickstart-events' , key= b'my_key', value= b'my_value2', partition= 0)
result = future.get(timeout= 10)
print(result)