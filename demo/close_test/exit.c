#include <linux/sched.h>
#include <uapi/linux/ptrace.h>

BPF_HASH(stats,u64 pid,u64 fd);


//TRACEPOINT_PROBE(syscalls, sys_enter_close) {
//    if (container_should_be_filtered()) {
//        return 0;
//    }


struct data_close {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
};

BPF_PERF_OUTPUT(close_events);


TRACEPOINT_PROBE(syscalls, sys_enter_close) {
//    if (container_should_be_filtered()) {
//        return 0;
//    }

    struct data_close data = {};
    u64 pid = bpf_get_current_pid_tgid();
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();
    data.fd = args->fd;


    stats.update(pid,fd);

    bpf_get_current_comm(&data.comm, sizeof(data.comm));


//    close_events.perf_submit(args, &data, sizeof(data));

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_close) {
//    if (container_should_be_filtered()) {
//        return 0;
//    }

    struct data_close data = {};
    u64 pid = bpf_get_current_pid_tgid();
    data.pid = pid;
    data.ts = bpf_ktime_get_ns();

    u32 ret = args->ret;

    if(ret != 0)//即调用close失败，删除map中对应的元素
        stats.delete(pid);
    else
    {
        data.fd = stats.lookup(pid);//调用成功拿到fd后 将data数据perf出去
        close_events.perf_submit(args, &data, sizeof(data));
    }


    bpf_get_current_comm(&data.comm, sizeof(data.comm));
    return 0;
}