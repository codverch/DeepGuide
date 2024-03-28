import os
import matplotlib.pyplot as plt
import re # Just in case

# ===========================================================================================================================

# Read 'categorized_lines.txt' file and find lines that contain 'network_keywords' and write them to 'found_network_keywords.txt'
with open('categorized_lines.txt', 'r') as file:
    lines = file.readlines()

if os.path.exists('found_network_keywords.txt'):
    os.remove('found_network_keywords.txt')

with open('found_network_keywords.txt', 'w') as file:
    write_next_line = False
    for line in lines:
        if 'network_keywords' in line:
            file.write(line)
            write_next_line = True
        elif write_next_line:
            file.write(line)
            write_next_line = False

# ===========================================================================================================================
# Read the 'found_network_keywords.txt' file.
# Extract the first part of each line.
# Initialize variables for tracking the previous branch stack number, function name, total CPU cycles taken, and category.
# Write the extracted data to the 'processed_found_network_keywords.txt' file, aggregating CPU cycles for lines with the same branch stack number.
# If a new branch stack number is encountered, write the aggregated data for the previous stack and reset the variables for the new chain.
# ===========================================================================================================================

# Read 'found_network_keywords.txt' file 
with open('found_network_keywords.txt', 'r') as file:
    lines = file.readlines()
    
# Extract the first part of the line
previous_branch_stack_num = None

with open('processed_found_network_keywords.txt', 'w') as outfile:
    for line in lines:
        branch_stack_num = line.split('-')[0].strip()
        function_name = line.split('-')[1].strip()
        total_cpu_cycles_taken = int(line.split('-')[2].strip())
        category = line.split('-')[3].strip()

        # If this is the first line then initialize the variables
        if previous_branch_stack_num is None:
            previous_branch_stack_num = branch_stack_num
            previous_function_name = function_name
            previous_total_cpu_cycles = total_cpu_cycles_taken
            previous_category = category
            continue


        # Check if branch stack num is the same as previous
        if branch_stack_num == previous_branch_stack_num:
            # Check if the category is the same as previous
            if category == previous_category:
                previous_total_cpu_cycles += int(total_cpu_cycles_taken)
            else:
                outfile.write(f"{previous_branch_stack_num} - {previous_function_name} - {previous_total_cpu_cycles} - {previous_category}\n")
                # Reset variables for the new chain with current values
                previous_total_cpu_cycles = int(total_cpu_cycles_taken)
                previous_category = category
                previous_branch_stack_num = branch_stack_num
                previous_function_name = function_name


        else:
            outfile.write(f"{previous_branch_stack_num} - {previous_function_name} - {previous_total_cpu_cycles} - {previous_category}\n")
            # Reset variables for the new chain with current values
            previous_total_cpu_cycles = int(total_cpu_cycles_taken)
            previous_category = category
            previous_branch_stack_num = branch_stack_num
            previous_function_name = function_name

# Read 'processed_found_network_keywords.txt' file
with open('processed_found_network_keywords.txt', 'r') as file:
    lines = file.readlines()

# Initialize a dictionary to store categories and their corresponding CPU cycles
category_cpu_cycles = {}

for line in lines:
    branch_stack_num = line.split('-')[0].strip()
    function_name = line.split('-')[1].strip()
    cpu_cycles = int(line.split('-')[2].strip())
    category = line.split('-')[3].strip()

    # Each network line is succeeded by a line belonging to a category that is not a network category
    # Plot the CPU cycles of the network category succeeed by the different categories
    # For example, CPU cycles taken by network_keywords + kernel_keywords, network_keywords + memory_keywords, etc.
    if category not in category_cpu_cycles:
        category_cpu_cycles[category] = cpu_cycles
    else :
        category_cpu_cycles[category] += cpu_cycles

# Calculate total CPU cycles
total_cpu_cycles = sum(category_cpu_cycles.values())
 
# Calculate percentage of CPU cycles for each category
category_cpu_percentages = {category: (cpu_cycles / total_cpu_cycles) * 100 for category, cpu_cycles in category_cpu_cycles.items()}

# Plot the percentage of CPU cycles of the network category succeeded by the different categories
categories = list(category_cpu_percentages.keys())
cpu_percentages = list(category_cpu_percentages.values())

plt.figure(figsize=(12, 6))
plt.bar(categories, cpu_percentages)
plt.xlabel('Category')
plt.ylabel('Percentage of CPU Cycles')
plt.title('Percentage of CPU Cycles by Category')
plt.xticks(rotation=45, ha='right')
plt.tight_layout()
plt.savefig('Random.png')
plt.show()

# ===========================================================================================================================
# Each line in the 'processed_found_network_keywords.txt' file follows a specific format:
#   - One line consists of 'network_keywords' followed by another line containing a category that is not classified as a network category.
# The objective is to visualize the percentage of CPU cycles attributed to the network category in conjunction with various other categories.
# It is important to note that no line in 'processed_found_network_keywords.txt' contains a network category followed by another network category.
# The desired graph should aggregate the CPU cycle counts from two consecutive lines whenever a network category is succeeded by a non-network category,
# illustrating the cumulative percentage of CPU cycles for the network category and the different subsequent categories.
# ===========================================================================================================================

# Read 'processed_found_network_keywords.txt' file
with open('processed_found_network_keywords.txt', 'r') as file:
    lines = file.readlines()

network_followed_by_category_cpu_cycles = {} 

for i in range(0, len(lines), 2):
    network_line = lines[i]
    if i + 1 < len(lines):
        category_line = lines[i + 1]
    else:
        # Handle case where there is no corresponding category line for the network line
        # For example, you could skip this network line or log a warning
        continue

    network_category = network_line.split('-')[3].strip()
    category = category_line.split('-')[3].strip()
    cpu_cycles = int(network_line.split('-')[2].strip()) + int(category_line.split('-')[2].strip())

    if network_category not in network_followed_by_category_cpu_cycles:
        network_followed_by_category_cpu_cycles[network_category] = {category: cpu_cycles}
    else:
        if category not in network_followed_by_category_cpu_cycles[network_category]:
            network_followed_by_category_cpu_cycles[network_category][category] = cpu_cycles
        else:
            network_followed_by_category_cpu_cycles[network_category][category] += cpu_cycles

#  Obtain the total cpu cycles from the 'categorized_lines.txt' file
total_cpu_cycles = 0
with open('categorized_lines.txt', 'r') as file:
    for line in file:
        parts = line.strip().split(' - ')
        if len(parts) > 2:
            cpu_cycle = parts[2].strip()
            if cpu_cycle.isdigit():
                total_cpu_cycles += int(cpu_cycle)

network_followed_by_category_cpu_percentages = {}
for network_category, categories in network_followed_by_category_cpu_cycles.items():
    network_followed_by_category_cpu_percentages[network_category] = {category: (cpu_cycles / total_cpu_cycles) * 100 for category, cpu_cycles in categories.items()}

# Plot the percentage of CPU cycles for each network category + category
plt.figure(figsize=(12, 6))
for network_category, categories in network_followed_by_category_cpu_percentages.items():
    plt.bar(categories.keys(), categories.values(), label=network_category)

plt.xlabel('Category')
plt.ylabel('Percentage of CPU Cycles')
plt.title('Percentage of CPU Cycles for Network Category Followed by Different Categories')
plt.xticks(rotation=45, ha='right')
plt.legend(title='Network Category')
plt.tight_layout()
# Print the percentage values on top of the bars
for network_category, categories in network_followed_by_category_cpu_percentages.items():
    for category, percentage in categories.items():
        plt.text(category, percentage, f'{percentage:.2f}%', ha='center', va='bottom')

plt.savefig('network_category_followed_by_category.png')
plt.show()

# ===========================================================================================================================
