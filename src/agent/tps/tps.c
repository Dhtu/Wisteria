#include <linux/sched.h>


// define output data structure in C

enum sys_call{
    read = 0,
    write = 1,
    socket = 2,
    close = 3,
    accept = 4,
    connect = 5,
    fork = 6
};

struct data_event {
    u32 pid;
    u64 enter_ts;
    u64 exit_ts;
    char comm[TASK_COMM_LEN];
    u64 fd;
    enum sys_call sys_call_id;
};
BPF_PERF_OUTPUT(events);

BPF_HASH(data_event_map,u32, struct data_event);

// write
TRACEPOINT_PROBE(syscalls, sys_enter_write) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = write;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_write) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}

//writev
TRACEPOINT_PROBE(syscalls, sys_enter_writev) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = write;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_writev) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}
//sendto
TRACEPOINT_PROBE(syscalls, sys_enter_sendto) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = write;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_sendto) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}

////sendmsg
TRACEPOINT_PROBE(syscalls, sys_enter_sendmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = write;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_sendmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}

//sendmmsg
TRACEPOINT_PROBE(syscalls, sys_enter_sendmmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = write;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_sendmmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}

//read
TRACEPOINT_PROBE(syscalls, sys_enter_read) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = read;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_read) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}


//recvfrom
TRACEPOINT_PROBE(syscalls, sys_enter_recvfrom) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = read;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_recvfrom) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}


//recvmsg
TRACEPOINT_PROBE(syscalls, sys_enter_recvmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = read;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_recvmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}

//recvmmsg
TRACEPOINT_PROBE(syscalls, sys_enter_recvmmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid=pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.fd = args->fd;
    data.sys_call_id = read;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));

    data_event_map.update(&pid,&data);

    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_recvmmsg) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;

    if(args->ret == -1){//即调用close失败，删除map中对应的元素
        data_event_map.delete(&pid);
    }
    else
    {
        struct data_event* p_data = (data_event_map.lookup(&pid));//调用成功拿到fd后 将data数据perf出去
        if (p_data == 0) {
            return 0;   // missed entry
        }
        p_data->exit_ts = bpf_ktime_get_ns();
        events.perf_submit(args, p_data, sizeof(*p_data));
    }
    return 0;
}


//socket
TRACEPOINT_PROBE(syscalls, sys_exit_socket) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.exit_ts = bpf_ktime_get_ns();
    data.fd = args->ret;
    data.sys_call_id = socket;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    events.perf_submit(args, &data, sizeof(data));

    return 0;
}


//close
BPF_HASH(stats,u32, u64);



TRACEPOINT_PROBE(syscalls, sys_enter_close) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;
    u64 fd = args->fd;
    stats.update(&pid,&fd);
    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_close) {

    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid()>>32;
    data.pid = pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.exit_ts = bpf_ktime_get_ns();
    data.sys_call_id = close;
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
        events.perf_submit(args, &data, sizeof(data));
        stats.delete(&pid);
    }
    return 0;
}

//accept
TRACEPOINT_PROBE(syscalls, sys_exit_accept) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.exit_ts = bpf_ktime_get_ns();
    data.fd = args->ret;
    data.sys_call_id = accept;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    events.perf_submit(args, &data, sizeof(data));

    return 0;
}

//accept4
TRACEPOINT_PROBE(syscalls, sys_exit_accept4) {
    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid() >> 32;
    data.pid = pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.exit_ts = bpf_ktime_get_ns();
    data.fd = args->ret;
    data.sys_call_id = accept;
    bpf_get_current_comm(&data.comm, sizeof(data.comm));


    events.perf_submit(args, &data, sizeof(data));

    return 0;
}



//clone
TRACEPOINT_PROBE(syscalls, sys_exit_clone) {
    if (container_should_be_filtered()) {
        return 0;
    }

    if (args->ret != 0){
        struct data_event data = {};
        u32 pid = bpf_get_current_pid_tgid() >> 32;
        data.pid = pid;
        data.enter_ts = bpf_ktime_get_ns();
        data.exit_ts = bpf_ktime_get_ns();
        data.fd = args->ret;
        data.sys_call_id = fork;
        bpf_get_current_comm(&data.comm, sizeof(data.comm));


        events.perf_submit(args, &data, sizeof(data));
    }

    return 0;
}

//fork
TRACEPOINT_PROBE(syscalls, sys_exit_fork) {
    if (container_should_be_filtered()) {
        return 0;
    }

    if (args->ret != 0){
        struct data_event data = {};
        u32 pid = bpf_get_current_pid_tgid() >> 32;
        data.pid = pid;
        data.enter_ts = bpf_ktime_get_ns();
        data.exit_ts = bpf_ktime_get_ns();
        data.fd = args->ret;
        data.sys_call_id = fork;
        bpf_get_current_comm(&data.comm, sizeof(data.comm));


        events.perf_submit(args, &data, sizeof(data));
    }

    return 0;
}

//vfork
TRACEPOINT_PROBE(syscalls, sys_exit_vfork) {
    if (container_should_be_filtered()) {
        return 0;
    }

    if (args->ret != 0){
        struct data_event data = {};
        u32 pid = bpf_get_current_pid_tgid() >> 32;
        data.pid = pid;
        data.enter_ts = bpf_ktime_get_ns();
        data.exit_ts = bpf_ktime_get_ns();
        data.fd = args->ret;
        data.sys_call_id = fork;
        bpf_get_current_comm(&data.comm, sizeof(data.comm));


        events.perf_submit(args, &data, sizeof(data));
    }

    return 0;
}


//connect
TRACEPOINT_PROBE(syscalls, sys_enter_connect) {
    if (container_should_be_filtered()) {
        return 0;
    }

    u32 pid = bpf_get_current_pid_tgid()>>32;
    u64 fd = args->fd;
    stats.update(&pid,&fd);
    return 0;
}

TRACEPOINT_PROBE(syscalls, sys_exit_connect) {

    if (container_should_be_filtered()) {
        return 0;
    }

    struct data_event data = {};
    u32 pid = bpf_get_current_pid_tgid()>>32;
    data.pid = pid;
    data.enter_ts = bpf_ktime_get_ns();
    data.exit_ts = bpf_ktime_get_ns();
    data.sys_call_id = connect;
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
        events.perf_submit(args, &data, sizeof(data));
        stats.delete(&pid);
    }
    return 0;
}