#!/bin/bash

if [ -f "instructions.txt" ]; then
    rm instructions.txt
fi

if [ -f "branch-misses.txt" ]; then
    rm branch-misses.txt
fi

if [ -f "processed_branch_stack.txt" ]; then
    rm processed_branch_stack.txt
fi

if [ -f "categorized_lines.txt" ]; then
    rm categorized_lines.txt
fi

if [ -f "uncategorized.txt" ]; then
    rm uncategorized.txt
fi

if [ -f "categorized_lines_plot.png" ]; then
    rm categorized_lines_plot.png
fi

if [ -f "branch_misses_percentage.png" ]; then
    rm branch_misses_percentage.png
fi

