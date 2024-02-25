# DeepGuide

## Prerequisites

Ensure you have `sudo` privileges and the `perf` tool installed on your system.

## Steps

1. **Record CPU cycles**: Use `perf` to record the process's CPU cycles.

    ```bash
    sudo perf record -j any_call,any_ret,save_type -e cpu-cycles -g -p <PID> -- sleep 60
    ```

    This command records the CPU cycles of the process with the given PID for 60 seconds, capturing function calls and returns.

2. **Change output file permissions**: The `perf record` command generates a `perf.data` file. Change its permissions to allow reading, writing, and executing.

    ```bash
    sudo chmod +rx perf.data
    ```

3. **Generate a performance report**: Use `perf script` to create a detailed report from `perf.data`.

    ```bash
    sudo perf script -i perf.data -F +brstacksym > branch_stack.txt
    ```

    The `-F +brstacksym` option includes branch stack symbols in the report.

4. **Categorize functions with extract.py**: Use `extract.py` to categorize top functions in the branch stack into tax categories or application logic. It produces `categorized_lines` and `uncategorized_lines` files. Manually categorize the keywords in `uncategorized_lines` into category files under `bucketization`.

Each line in the output represents a sample.

5. **Plot CPU cycles**: Use the script `plot_cpu_cycles.py` to generate two PNG images: `cpu_cycles.png` and `cpu_cycles_percentage.png`, representing the raw values of CPU cycles and the percentage of CPU cycles for each tax category respectively.
