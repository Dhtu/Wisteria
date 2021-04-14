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
struct data_sock {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
};
BPF_PERF_OUTPUT(sock_events);

//socket
TRACEPOINT_PROBE(syscalls, sys_exit_socket) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_sock data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->ret;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    sock_events.perf_submit(args, &data, sizeof(data));

    return 0;
}
"""

prog = filter_by_containers(args) + prog

# load BPF program
b = BPF(text=prog)

# header
print("%-18s %-16s %-6s %s" % ("TIME(s)", "COMM", "PID", "GOTBITS"))


def print_event(cpu, data, size):
    event = b["sock_events"].event(data)
    print("%-18.9f %-16s %-6d %-6d" % (event.ts, event.comm, event.pid,event.fd))

b["sock_events"].open_perf_buffer(print_event)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
