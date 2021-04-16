#include <linux/sched.h>


// define output data structure in C

struct data_write {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
};
BPF_PERF_OUTPUT(write_events);


struct data_read {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
};
BPF_PERF_OUTPUT(read_events);


// write
TRACEPOINT_PROBE(syscalls, sys_enter_write) {
    if (container_should_be_filtered()) {
        return 0;
    }
    struct data_write data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    write_events.perf_submit(args, &data, sizeof(data));
    return 0;
}


//writev
TRACEPOINT_PROBE(syscalls, sys_enter_writev) {
    if (container_should_be_filtered()) {
        return 0;
    }
    struct data_write data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    write_events.perf_submit(args, &data, sizeof(data));
    return 0;
}

//sendto
TRACEPOINT_PROBE(syscalls, sys_enter_sendto) {
    if (container_should_be_filtered()) {
        return 0;
    }
    struct data_write data = {};
    u32 pid = bpf_get_current_pid_tgid()>>32;
    data.pid=pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    write_events.perf_submit(args, &data, sizeof(data));
    return 0;
}

//sendmsg
TRACEPOINT_PROBE(syscalls, sys_enter_sendmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }
    struct data_write data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    write_events.perf_submit(args, &data, sizeof(data));
    return 0;
}

//sendmmsg
TRACEPOINT_PROBE(syscalls, sys_enter_sendmmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }
    struct data_write data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    write_events.perf_submit(args, &data, sizeof(data));
    return 0;
}

//read
TRACEPOINT_PROBE(syscalls, sys_enter_read) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_read data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    read_events.perf_submit(args, &data, sizeof(data));

    return 0;
}

//readv
TRACEPOINT_PROBE(syscalls, sys_enter_readv) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_read data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    read_events.perf_submit(args, &data, sizeof(data));

    return 0;
}


//recvfrom
TRACEPOINT_PROBE(syscalls, sys_enter_recvfrom) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_read data = {};
    data.pid = bpf_get_current_pid_tgid()>>32;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    read_events.perf_submit(args, &data, sizeof(data));

    return 0;
}

//recvmsg
TRACEPOINT_PROBE(syscalls, sys_enter_recvmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_read data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    read_events.perf_submit(args, &data, sizeof(data));

    return 0;
}

//recvmmsg
TRACEPOINT_PROBE(syscalls, sys_enter_recvmmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_read data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    read_events.perf_submit(args, &data, sizeof(data));

    return 0;
}


//socket
struct data_sock {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
};
BPF_PERF_OUTPUT(sock_events);


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


//close
struct data_close {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
};
BPF_PERF_OUTPUT(close_events);

BPF_HASH(stats,u32, u64);



TRACEPOINT_PROBE(syscalls, sys_enter_close) {

    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid();
    u64 fd = args->fd;
    stats.update(&pid,&fd);
    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_close) {

    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_close data = {};
    u32 pid = bpf_get_current_pid_tgid();
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    long ret = args->ret;

    if(args->ret != 0)//即调用close失败，删除map中对应的元素
        stats.delete(&pid);
    else
    {
        u64* fd = (stats.lookup(&pid));//调用成功拿到fd后 将data数据perf出去

        if (fd == 0) {
            return 0;   // missed entry
        }
        data.fd = *fd;
        close_events.perf_submit(args, &data, sizeof(data));
    }
    return 0;
}

//accept

struct data_accept {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
};
BPF_PERF_OUTPUT(accept_events);

TRACEPOINT_PROBE(syscalls, sys_exit_accept) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_accept data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->ret;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    accept_events.perf_submit(args, &data, sizeof(data));

    return 0;
}

//accept4
TRACEPOINT_PROBE(syscalls, sys_exit_accept4) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_accept data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->ret;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    accept_events.perf_submit(args, &data, sizeof(data));

    return 0;
}


struct data_fork {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    long ret;
};
BPF_PERF_OUTPUT(fork_events);

//fork
TRACEPOINT_PROBE(syscalls, sys_exit_clone) {
    if (container_should_be_filtered()) {
        return 0;
    }

    if (args->ret != 0){
        struct data_fork data = {};
        u32 pid = bpf_get_current_pid_tgid() >> 32;
        data.pid = pid;
        data.ts = bpf_ktime_get_ns();
        data.ret = args->ret;
        bpf_get_current_comm(&data.comm, sizeof(data.comm));


        fork_events.perf_submit(args, &data, sizeof(data));
    }

    return 0;
}