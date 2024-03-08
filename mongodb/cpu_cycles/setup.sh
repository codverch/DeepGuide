#!/bin/bash

# Change ownership of perf.data to your 'username'
sudo chown deepmish perf.data

# Add execute permission to perf.data
sudo chmod +x perf.data

# Extract the branch stacks
sudo perf script -i perf.data -F brstacksym > branch_stack.txt -f

#  Plot the CPU cycles

# Install matplotlib
pip3 install matplotlib

sudo python3 plot_cpu_cycles.py