#!/bin/bash

# Remove existing text files if they exist
rm -f instructions.txt
rm -f L1-icache-load-misses.txt

# Run perf script
sudo perf script -i perf.data -F brstacksym -v --per-event-dump -f

# Copy instructions
cat perf.data.instructions.dump > instructions.txt

# Copy L1-icache-load-misses
cat perf.data.L1-icache-load-misses.dump > L1-icache-load-misses.txt

# Run plot_l1_icache_misses.py
python3 plot_l1_icache_misses.py