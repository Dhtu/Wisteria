#include <linux/sched.h>
#include <uapi/linux/ptrace.h>

BPF_HASH(stats,u32, u64);

struct data_close {
    u32 pid;
    u64 ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
    long ret;
};

BPF_PERF_OUTPUT(close_events);


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
    data.ret = ret;

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