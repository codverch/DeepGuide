# DeepGuide

## Directory Structure

```
DeepGuide
├── commands
├── memcached
│   ├── branch_misses
│   │   └── bucketization
│   ├── cpu_cycles
│   │   └── bucketization
│   ├── l1_icache_load_misses
│   │   └── bucketization
│   └── llc_load_misses
│       └── bucketization
├── mongodb
│   ├── branch_misses
│   │   └── bucketization
│   ├── cpu_cycles
│   │   └── bucketization
│   ├── l1_icache_misses
│   │   └── bucketization
│   └── llc_load_misses
│       └── bucketization
└── README.md
```

## Prerequisites

Ensure you have `sudo` privileges and the `perf` tool installed on your system.

## Steps

1. **Record Perf Samples**: Use the following commands to record performance samples for each application. Replace `<PID>` with the actual PID of the process.

    ```bash
    # Record CPU cycles 
    sudo perf record -j any_call,any_ret,save_type -e cpu-cycles -g -p <Memcached/MongoDB_PID> -- sleep 300

    # Record branch misses 
    sudo perf record -j any_call,any_ret,save_type -e branch-misses,instructions -g -p <Memcached/MongoDB_PID> -- sleep 300

    # Record L1 instruction cache load misses 
    sudo perf record -j any_call,any_ret,save_type -e L1-icache-load-misses,instructions -g -p <Memcached/MongoDB_PID> -- sleep 300

    # Record last-level cache load misses 
    sudo perf record -j any_call,any_ret,save_type -e LLC-load-misses,instructions -g -p <Memcached/MongoDB_PID> -- sleep 300
    ```

 These commands record performance samples for CPU cycles, branch misses, L1 instruction cache load misses, and last-level cache load misses for Memcached and MongoDB. Make sure to replace `<Memcached_PID>` and `<MongoDB_PID>` with the actual PIDs of your Memcached and MongoDB processes.

2. **Generate Graphs**: Run the `setup.sh` script in each sub-directory (`cpu_cycles`, `branch_misses`, `l1_icache_load_misses`, `llc_load_misses`) to generate the graphs.

    ```bash
    cd memcached/cpu_cycles && ./setup.sh
    cd memcached/branch_misses && ./setup.sh
    cd memcached/l1_icache_load_misses && ./setup.sh
    cd memcached/llc_load_misses && ./setup.sh

    cd mongodb/cpu_cycles && ./setup.sh
    cd mongodb/branch_misses && ./setup.sh
    cd mongodb/l1_icache_load_misses && ./setup.sh
    cd mongodb/llc_load_misses && ./setup.sh
    ```

    The `setup.sh` script will generate the required graphs for each performance metric.