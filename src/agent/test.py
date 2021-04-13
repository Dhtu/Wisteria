#!/usr/bin/python
from __future__ import print_function
from bcc import BPF
from bcc import BPF
from bcc.containers import filter_by_containers
import argparse

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

# load BPF program
prog="""
#include <linux/sched.h>
struct data_write {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    int bits;
};
BPF_PERF_OUTPUT(events);


TRACEPOINT_PROBE(syscalls, sys_enter_write) {
    struct data_write data = {};
    u32 pid = bpf_get_current_pid_tgid();
    data.pid=pid;
    data.ts = bpf_ktime_get_ns();
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    events.perf_submit(args, &data, sizeof(data));
    return 0;
}
"""

prog = filter_by_containers(args) + prog

# load BPF program
b = BPF(text=prog)

# header
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "GOTBITS"))


def print_event(cpu, data, size):
    event = b["events"].event(data)
    # print("%-18.9f %-16s %-6d %s" % (event.ts, event.comm, event.pid, event.bits))

b["events"].open_perf_buffer(print_event)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
