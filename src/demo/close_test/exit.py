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
filename = module_path + '/exit.c'
with open(filename, mode="r") as file:
    prog = file.read()

prog = filter_by_containers(args) + prog

# load BPF program
b = BPF(text=prog)

# header
print("Start monitoring the sys_read system call")


def sys_exit_close(cpu, data, size):
    event = b["close_events"].event(data)
    # ebpf_event_listener.on_close(event)
    print("hello")
    print(event.pid)
    print(event.fd)

b["close_events"].open_perf_buffer(sys_exit_close)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
