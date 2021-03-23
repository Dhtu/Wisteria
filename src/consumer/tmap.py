#!/usr/bin/python3

class connect_edge:
    saddr = ''
    daddr = ''
    dport = ''

    def __init__(self, saddr, daddr, dport):
        self.saddr = saddr
        self.daddr = daddr
        self.dport = dport

    def __hash__(self):
        return hash(self.saddr+self.daddr+self.dport)

    def __eq__(self, other):
        return (self.saddr, self.daddr, self.dport) == (other.saddr, other.daddr, other.dport)

    def __ne__(self, other):
        # Not strictly necessary, but to avoid having both x==y and x!=y
        # True at the same time
        return not (self == other)


class topology_map:
    m_map = dict()

    def add(self,key):
        if key in self.m_map:
            self.m_map[key] +=1
        else:
            self.m_map[key] = 1