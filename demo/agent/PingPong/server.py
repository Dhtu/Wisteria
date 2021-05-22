#!/usr/bin/env python
import time,math,random
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

from pygen.ping import PingService


class PingServiceHandler:
    def __init__(self):
        self.log = {}
        self.count = random.randint(0,62)

    def ping(self):
        return 'pong'

    def say(self, msg):
        self.count+=1
        time.sleep((math.sin(self.count/10)+1))
        print(msg+str(math.sin(self.count/10)+1))


handler = PingServiceHandler()
processor = PingService.Processor(handler)
transport = TSocket.TServerSocket(port=9091 )
tfactory = TTransport.TBufferedTransportFactory()
pfactory = TBinaryProtocol.TBinaryProtocolFactory()

server = TServer.TSimpleServer(processor, transport, tfactory, pfactory)

print('Starting python server...')
server.serve()
print('done!')