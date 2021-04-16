class tps_item:
    ts = 0
    pid = 0
    is_read = True
    ip = ''

    def __init__(self, t, p, r, i):
        self.ts = float(t)
        self.pid = int(p)
        self.is_read = r == 'read'
        self.ip = i


class tps_counter:
    num = 0
    ts = 0
    write_table = dict()
    ip = ''

    def __init__(self, ip):
        self.ip = ip

    def add_item(self, item):
        if item.is_read == False:
            self.write_table[item.pid] = item.ts
        else:
            if item.pid in self.write_table:
                self.num += 1
                self.ts += (item.ts - self.write_table[item.pid])
                del self.write_table[item.pid]

    def get_tps(self):
        return self.num

    def get_delay(self):
        if self.num == 0:
            return -1
        else:
            return self.ts / self.num


class tps_table:
    m_table = dict()

    def add_item(self, item):
        if item.ip not in self.m_table:
            self.m_table[item.ip] = tps_counter(item.ip)

        self.m_table[item.ip].add_item(item)

    def get_tps(self,ip):
        return self.m_table[ip].get_tps()

    def get_delay(self,ip):
        return self.m_table[ip].get_delay()