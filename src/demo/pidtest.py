#!/usr/bin/python
from bcc import BPF
BPF(text='TRACEPOINT_PROBE(syscalls, sys_exit_fork) { bpf_trace_printk("Hello, World!\\n"); return 0; }').trace_print()