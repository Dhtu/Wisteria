#!/usr/bin/env python

import sys
sys.path.append('pygen')

from thrift import Thrift
from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol

from pygen.ping import PingService

try:

    # Make socket
    transport = TSocket.TSocket('172.17.0.1', 9091)

    # Buffering is critical. Raw sockets are very slow
    transport = TTransport.TBufferedTransport(transport)

    # Wrap in a protocol
    protocol = TBinaryProtocol.TBinaryProtocol(transport)

    # Create a client to use the protocol encoder
    client = PingService.Client(protocol)

    # Connect!
    transport.open()
    print(client.ping())
    client.say('Hello from python!')
    client.say('Hello from python2!')
    client.say('Hello from python3!')

    # Close!
    transport.close()

except Thrift.TException as tx:
    print('%s' % (tx.message))