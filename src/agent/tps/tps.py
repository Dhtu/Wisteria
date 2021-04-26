#!/usr/bin/python

import os
from bcc import BPF
from bcc.containers import filter_by_containers
import argparse

from eBPF_event_listener import ebpf_event_listener

# arguments
examples = """examples:
    ./tps           # trace system tps
    ./tps --cgroupmap mappath  # only trace cgroups in this BPF map
    ./tps --mntnsmap mappath   # only trace mount namespaces in the map
"""

parser = argparse.ArgumentParser(
    description="Trace system tps",
    formatter_class=argparse.RawDescriptionHelpFormatter,
    epilog=examples)
parser.add_argument("--cgroupmap",
                    help="trace cgroups in this BPF map only")
parser.add_argument("--mntnsmap",
                    help="trace mount namespaces in this BPF map only")
args = parser.parse_args()

# read BPF program
module_path = os.path.dirname(__file__)
filename = module_path + '/tps.c'
with open(filename, mode="r") as file:
    prog = file.read()

prog = filter_by_containers(args) + prog

# load BPF program
b = BPF(text=prog)

# header
print("Start monitoring the system tps")

event_time = -1000
c = 0


def process_events(ctx, data, size):
    event = b["events"].event(data)
    ebpf_event_listener.routing(event)

    # global event_time
    # global c
    # if event_time<=event.exit_ts:
    #     event_time = event.exit_ts
    #     c += 1
    #     print(c)
    # else:
    #     print("error min time: %-9.3f event time: %-9.3f" % (event_time,event.exit_ts))
    #     exit()


b["events"].open_ring_buffer(process_events)

while True:
    try:
        b.ring_buffer_poll()
    except KeyboardInterrupt:
        exit()
