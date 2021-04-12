#include <linux/sched.h>


// define output data structure in C

struct data_write {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    unsigned int fd;
};
BPF_PERF_OUTPUT(write_events);


struct data_read {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    unsigned int fd;
};
BPF_PERF_OUTPUT(read_events);



TRACEPOINT_PROBE(syscalls, sys_enter_write) {
    if (container_should_be_filtered()) {
        return 0;
    }


    struct data_write data = {};

    u32 pid = bpf_get_current_pid_tgid();
    data.pid=pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    write_events.perf_submit(args, &data, sizeof(data));

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_enter_read) {
    if (container_should_be_filtered()) {
        return 0;
    }


    struct data_read data = {};


    data.pid = bpf_get_current_pid_tgid();
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    read_events.perf_submit(args, &data, sizeof(data));

    return 0;
}