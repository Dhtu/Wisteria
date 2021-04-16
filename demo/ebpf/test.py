#!/usr/bin/python
from bcc import BPF


# load BPF program
prog="""
#include <linux/sched.h>

struct data_fork {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    long ret;
};
BPF_PERF_OUTPUT(fork_events);


//fork
TRACEPOINT_PROBE(syscalls, sys_exit_fork) {


    struct data_fork data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.ret = args->ret;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    fork_events.perf_submit(args, &data, sizeof(data));



    return 0;
}


"""

# load BPF program
b = BPF(text=prog)


def print_event(cpu, data, size):
    event = b["fork_events"].event(data)
    print("%-18.9f %-16s %-6d %-6d" % (event.ts, event.comm, event.pid,event.ret))

b["fork_events"].open_perf_buffer(print_event)

while True:
    try:
        b.perf_buffer_poll()
    except KeyboardInterrupt:
        exit()
