import os
import matplotlib.pyplot as plt

# Define your network keywords here
network_keywords = ["network_keywords"]

# Read the contents of categorized_lines.txt
with open('categorized_lines.txt', 'r') as file:
    lines = file.readlines()

if os.path.exists('preceeded.txt'):
    os.remove('preceeded.txt')

# Initialize variables to keep track of consecutive functions
previous_branch_stack_num = None
previous_function_name = None
previous_total_cpu_cycles = 0
previous_category = None

# Initialize a dictionary to count network keywords preceded by categories
network_keyword_counts = {keyword: 0 for keyword in network_keywords}

# Open a new file called "preceeded.txt" for writing
with open('preceeded.txt', 'w') as outfile:
    # Process each line
    for line in lines:
        parts = line.split('-')
        if len(parts) >= 4:
            branch_stack_num = parts[0].strip()
            function_name = parts[1].strip()
            total_cpu_cycles_taken = int(parts[2].strip())
            category = parts[3].strip()

            # Check if this is the first line
            if previous_branch_stack_num is None:
                previous_branch_stack_num = branch_stack_num
                previous_function_name = function_name
                previous_total_cpu_cycles = total_cpu_cycles_taken
                previous_category = category
                continue

            # Check if branch stack num is the same as previous
            if branch_stack_num == previous_branch_stack_num:
                # Check if category is the same as previous
                if category == previous_category:
                    # Add total cpu cycles to previous
                    previous_total_cpu_cycles += total_cpu_cycles_taken
                else:
                    # Count network keywords preceded by the previous category
                    for keyword in network_keywords:
                        if keyword in previous_category:
                            network_keyword_counts[keyword] += 1

                    # Write previous entry to "preceeded.txt"
                    outfile.write(f"{previous_branch_stack_num} - {previous_function_name} - {previous_total_cpu_cycles} - {previous_category}\n")
                    # Reset variables for the new chain
                    previous_function_name = function_name
                    previous_total_cpu_cycles = total_cpu_cycles_taken
                    previous_category = category
            else:
                # Count network keywords preceded by the previous category
                for keyword in network_keywords:
                    if keyword in previous_category:
                        network_keyword_counts[keyword] += 1

                # Write previous entry to "preceeded.txt"
                outfile.write(f"{previous_branch_stack_num} - {previous_function_name} - {previous_total_cpu_cycles} - {previous_category}\n")
                # Reset variables for the new chain
                previous_branch_stack_num = branch_stack_num
                previous_function_name = function_name
                previous_total_cpu_cycles = total_cpu_cycles_taken
                previous_category = category

    # Write the last entry
    if previous_branch_stack_num is not None:
        outfile.write(f"{previous_branch_stack_num} - {previous_function_name} - {previous_total_cpu_cycles} - {previous_category}\n")



def count_network_keywords_preceded_by_category(input_filename):
    # Initialize a dictionary to store the counts and CPU cycles
    category_network_keyword_counts = {}

    # Open the input file for reading
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    # Initialize variables to keep track of the previous line's branch stack number and category
    previous_branch_stack_num = None
    previous_category = None
    cpu_cycles = 0

    # Process each line
    for line in lines:
        parts = line.split('-')
        if len(parts) >= 4:
            branch_stack_num = parts[0].strip()
            function_name = parts[1].strip()
            total_cpu_cycles_taken = int(parts[2].strip())
            category = parts[3].strip()

            # Check if this is the first line
            if previous_branch_stack_num is None:
                previous_branch_stack_num = branch_stack_num
                previous_category = category
                cpu_cycles += total_cpu_cycles_taken
                continue

            # Check if branch stack num is the same as previous
            if branch_stack_num == previous_branch_stack_num:
                if previous_category not in category_network_keyword_counts:
                    category_network_keyword_counts[previous_category] = {'count': 0, 'cpu_cycles': 0}

                # Check if network keywords are present in the current function's category
                for keyword in network_keywords:
                    if keyword in category:
                        category_network_keyword_counts[previous_category]['count'] += 1
                        category_network_keyword_counts[previous_category]['cpu_cycles'] += cpu_cycles

                cpu_cycles += total_cpu_cycles_taken
                # Update the previous category
                previous_category = category

            else:
                if previous_category not in category_network_keyword_counts:
                    category_network_keyword_counts[previous_category] = {'count': 0, 'cpu_cycles': 0}

                # Check if network keywords are present in the current function's category
                for keyword in network_keywords:
                    if keyword in category:
                        category_network_keyword_counts[previous_category]['count'] += 1
                        category_network_keyword_counts[previous_category]['cpu_cycles'] += cpu_cycles

                cpu_cycles = total_cpu_cycles_taken
                previous_branch_stack_num = branch_stack_num
                previous_category = category

    # Print the counts of network keywords preceded by categories
    for category, counts in category_network_keyword_counts.items():
        print(f"Category: {category}")
        print(f"Network Keywords Count: {counts['count']}")
        print(f"CPU Cycles: {counts['cpu_cycles']}")

def plot_cpu_cycles_vs_category(input_filename):
    category_network_keyword_counts = {}
    with open(input_filename, 'r') as file:
        lines = file.readlines()

    previous_branch_stack_num = None
    previous_category = None
    cpu_cycles = 0

    for line in lines:
        parts = line.split('-')
        if len(parts) >= 4:
            branch_stack_num = parts[0].strip()
            function_name = parts[1].strip()
            total_cpu_cycles_taken = int(parts[2].strip())
            category = parts[3].strip()

            if previous_branch_stack_num is None:
                previous_branch_stack_num = branch_stack_num
                previous_category = category
                cpu_cycles += total_cpu_cycles_taken
                continue

            if branch_stack_num == previous_branch_stack_num:
                if previous_category not in category_network_keyword_counts:
                    category_network_keyword_counts[previous_category] = {'count': 0, 'cpu_cycles': 0}

                for keyword in network_keywords:
                    if keyword in category:
                        category_network_keyword_counts[previous_category]['count'] += 1
                        category_network_keyword_counts[previous_category]['cpu_cycles'] += cpu_cycles

                cpu_cycles += total_cpu_cycles_taken
                previous_category = category

            else:
                if previous_category not in category_network_keyword_counts:
                    category_network_keyword_counts[previous_category] = {'count': 0, 'cpu_cycles': 0}

                for keyword in network_keywords:
                    if keyword in category:
                        category_network_keyword_counts[previous_category]['count'] += 1
                        category_network_keyword_counts[previous_category]['cpu_cycles'] += cpu_cycles

                cpu_cycles = total_cpu_cycles_taken
                previous_branch_stack_num = branch_stack_num
                previous_category = category

    categories = []
    cpu_cycles_list = []
    for category, counts in category_network_keyword_counts.items():
        categories.append(category)
        cpu_cycles_list.append(counts['cpu_cycles'])

    plt.figure(figsize=(12, 6))
    plt.bar(categories, cpu_cycles_list)
    plt.xlabel('Category')
    plt.ylabel('CPU Cycles')
    plt.title('CPU Cycles vs. Category')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig('cpu_cycles_vs_category.png')
    plt.show()


# Example usage
input_filename = 'preceeded.txt'
count_network_keywords_preceded_by_category(input_filename)

plot_cpu_cycles_vs_category(input_filename)


