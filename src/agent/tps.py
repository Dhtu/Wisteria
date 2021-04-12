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
print("Start monitoring the sys_read system call")


def print_write_event(cpu, data, size):
    event = b["write_events"].event(data)
    ebpf_event_listener.on_write(event)


def print_read_event(cpu, data, size):
    event = b["read_events"].event(data)
    ebpf_event_listener.on_read(event)


# loop with callback to print_event
b["read_events"].open_perf_buffer(print_read_event)
b["write_events"].open_perf_buffer(print_write_event)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
