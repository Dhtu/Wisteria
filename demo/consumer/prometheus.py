#!/usr/bin/python

from prometheus_client import Counter, Gauge, Summary, Histogram, start_http_server

# need install prometheus_client

if __name__ == '__main__':
    c = Counter('cc', 'A counter')
    c.inc()

    g = Gauge('gg', 'A gauge')
    g.set(17)

    s = Summary('ss', 'A summary', ['a', 'b'])
    s.labels('c', 'd').observe(17)

    h = Histogram('hh', 'A histogram')
    h.observe(.6)

    start_http_server(8000)
    import time

    while True:
        time.sleep(1)