import re
import os
import matplotlib.pyplot as plt

# Remove the files if they exist

if os.path.exists('processed_branch_stack.txt'):
    os.remove('processed_branch_stack.txt')
if os.path.exists('categorized_lines.txt'):
    os.remove('categorized_lines.txt')
if os.path.exists('uncategorized.txt'):
    os.remove('uncategorized.txt')
if os.path.exists('app_logic_vs_orchestration.png'):
    os.remove('app_logic_vs_orchestration.png')
if os.path.exists('tax_breakdown.png'):
    os.remove('tax_breakdown.png')

def process_file():
    """
    Process each line in 'branch_stack.txt', extract function names, and write them to 'processed_branch_stack.txt' along with CPU cycle values.
    """
    with open('branch_stack.txt', 'r') as file:
        lines = file.readlines()

    with open('processed_branch_stack.txt', 'w') as outfile:
        for line in lines:
            if not line.strip():  # Skip empty lines
                continue

            segments = line.strip().split()
            for segment in segments:
                parts = segment.split('/')
                if len(parts) >= 2:
                    from_function_with_address = parts[0]
                    from_function_match = re.match(r'([^\+]+)', from_function_with_address)
                    if from_function_match:
                        from_function = from_function_match.group(1)
                        cpu_cycle = parts[-1]
                        outfile.write(f"{from_function} - {cpu_cycle}\n")

def bucketize_lines():
    """
    Categorize lines in 'processed_branch_stack.txt' based on keywords in bucket files.
    Write categorized lines to 'categorized_lines.txt' and uncategorized lines to 'uncategorized_lines.txt'.
    """
    bucketization_folder = 'bucketization'
    bucket_files = [file_name for file_name in os.listdir(bucketization_folder)]
    bucket_file_contents = {}

    for bucket_keywords in bucket_files:
        with open(os.path.join(bucketization_folder, bucket_keywords), 'r') as file:
            bucket_file_contents[bucket_keywords] = [line.split("#")[0].strip() for line in file.readlines()]

    with open('processed_branch_stack.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("["):
                if line.startswith("[unknown]"):
                    parts = line.split('/')
                    if len(parts) > 5:
                        cpu_cycle = parts[5].split()[0]
                    else:
                        cpu_cycle = "unknown"
                    with open(f"categorized_lines.txt", 'a') as file:
                        file.write(f"[unknown] - {cpu_cycle} - application_logic_keywords\n")
            else:
                line_processed = line.split(" ", 1)[0]
                found = False
                for bucket_file in bucket_files:
                    if line_processed in bucket_file_contents[bucket_file]:
                        found = True
                        with open(f"categorized_lines.txt", 'a') as file:
                            file.write(f"{line.strip()} - {bucket_file}\n")
                        break
                if not found:
                    with open("uncategorized.txt", 'a') as file:
                        if line.strip():
                            file.write(line + '\n')

def plot_app_logic_vs_orchestration():
    """
    Plot the percentage of CPU cycles used by application logic vs. orchestration work.
    """
    categories_cpu_cycles = {'application_logic': 0, 'orchestration_work': 0}
    
    with open('categorized_lines.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) > 2:
                category = parts[2].strip()
                cpu_cycle = parts[1].strip()
                if cpu_cycle.isdigit():
                    cpu_cycle = int(cpu_cycle)
                    if category == 'application_logic_keywords':
                        categories_cpu_cycles['application_logic'] += cpu_cycle
                    else:
                        categories_cpu_cycles['orchestration_work'] += cpu_cycle

    total_cycles = sum(categories_cpu_cycles.values())
    percentages = {k: (v / total_cycles) * 100 for k, v in categories_cpu_cycles.items()}

    labels = percentages.keys()
    sizes = percentages.values()
    colors = ['black', 'red']

    plt.figure(figsize=(10, 7))
    bars = plt.bar(labels, sizes, color=colors)
    plt.xlabel('Categories')
    plt.ylabel('Percentage of CPU Cycles')
    plt.title('CPU Cycle Usage: Application Logic vs Orchestration Work (MongoDB)')
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')

    plt.savefig('app_logic_vs_orchestration.png')
    plt.close()

def plot_tax_breakdown():
    """
    Plot the percentage of CPU cycles used by different categories.
    """
    categories = {}

    with open('categorized_lines.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) > 2:
                category = parts[-1].strip()
                cpu_cycle = parts[1].strip()
                if cpu_cycle.isdigit():
                    cpu_cycle = int(cpu_cycle)
                    if category not in categories:
                        categories[category] = cpu_cycle
                    else:
                        categories[category] += cpu_cycle

    total_cycles = sum(categories.values())
    percentages = {k: (v / total_cycles) * 100 for k, v in categories.items()}
    sorted_categories = dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))

    plt.figure(figsize=(12, 8))
    bars = plt.bar(sorted_categories.keys(), sorted_categories.values(), color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Percentage of CPU Cycles')
    plt.title('CPU Cycle Usage: Tax Breakdown (MongoDB)')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')

    plt.savefig('tax_breakdown.png')
    plt.close()

# Call the functions
process_file()
bucketize_lines()
plot_app_logic_vs_orchestration()
plot_tax_breakdown()
