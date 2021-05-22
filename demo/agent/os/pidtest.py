#!/usr/bin/python
from bcc import BPF
print("hello")
BPF(text='TRACEPOINT_PROBE(syscalls, sys_enter_fork) { bpf_trace_printk("Hello, World!\\n"); return 0; }').trace_print()