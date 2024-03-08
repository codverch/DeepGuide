#!/bin/bash

# Change ownership of perf.data to your 'username'
sudo chown deepmish perf.data

# Add execute permission to perf.data
sudo chmod +x perf.data

# Remove existing text files if they exist
rm -f instructions.txt
rm -f LLC-load-misses.txt

# Run perf script
sudo perf script -i perf.data -F brstacksym -v --per-event-dump -f

# Copy instructions
cat perf.data.instructions.dump > instructions.txt

# Copy LLC-load-misses
cat perf.data.LLC-load-misses.dump > LLC-load-misses.txt

# Run plot_llc_load_misses.py
python3 plot_llc_load_misses.py