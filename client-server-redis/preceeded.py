import os
import matplotlib.pyplot as plt
import re 


def process_file():
    with open('branch_stack.txt', 'r') as file:
        lines = file.readlines()

    # Extract: from_function_name - branch_stack_number - cpu_cycle
    with open('processed_branch_stack.txt', 'w') as outfile:
        for idx, line in enumerate(lines, start=1): 
            # Skip empty lines
            if not line.strip():
                continue
            
            # Split the line into individual function calls
            segments = line.strip().split()

            # Process each segment to find "from" functions
            for segment in segments:
                # Split each segment by '/' to separate "from" and "to" functions
                parts = segment.split('/')
                # Ensure we have at least one '/' to split "from" and "to" functions
                if len(parts) >= 2:
                    # The "from" function and address are in the first part
                    from_function_with_address = parts[0]
                    # Extract the "from" function name, ignoring the address
                    from_function_match = re.match(r'([^\+]+)', from_function_with_address)
                    if from_function_match:
                        from_function = from_function_match.group(1)
                        # The CPU cycle is in the last part of the segment
                        cpu_cycle = parts[-1]
                        # Write "from" function and branch stack number to the file
                        outfile.write(f"{from_function} - Branch Stack Number: {idx} - {cpu_cycle}\n")

                        # Open the extracted_from_functions.txt file in append mode
                        with open('extracted_from_functions.txt', 'a') as func_outfile:
                            # Write "from" function and branch stack number to the extracted functions file
                            func_outfile.write(f"{from_function} - Branch Stack Number: {idx} - {cpu_cycle}\n")

def categorize_functions():
    # Path to the bucketization folder
    bucketization_folder = 'bucketization'

    # Bucket files
    bucket_files = [file_name for file_name in os.listdir(bucketization_folder)]

    # Dictionary to store the processed contents of each bucket file
    bucket_file_contents = {}

    # Fetch all the keywords from the bucket files and process them
    for bucket_keywords in bucket_files:
        with open(os.path.join(bucketization_folder, bucket_keywords), 'r') as file:
            bucket_file_contents[bucket_keywords] = [line.split("#")[0].strip() for line in file.readlines()]
    
    # Categorize the lines in the 'processed_branch_stack.txt' file
    with open('processed_branch_stack.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Process lines that start with '[' as 'application_logic'
            if line.startswith("["):
                # For lines starting with "[unknown]", extract the CPU cycle value for the first function and write the formatted line
                if line.startswith("[unknown]"):
                    parts = line.split('/')
                    if len(parts) > 5:
                        cpu_cycle = parts[5].split()[0]
                        branch_stack_number = parts[3].split()[0]
                    else:
                        cpu_cycle = "unknown"
                    with open(f"categorized_lines.txt", 'a') as file:
                        file.write(f"[unknown] - Branch Stack Number: {branch_stack_number} - {cpu_cycle} - application_logic_keywords\n")
            else:
                # Split the line at the first space to exclude the CPU cycle value
                line_processed = line.split(" ", 1)[0].strip() # strip to remove leading/trailing whitespaces
                # Check if this processed line is present in any of the bucket files as a substring
                found = False
                for bucket_file in bucket_files:
                    # Check if any keyword from the bucket file is a substring of the processed line
                    for bucket_line in bucket_file_contents[bucket_file]:
                        if bucket_line in line_processed: # If a line in the bucket file is found in the processed line (substring match)
                            found = True
                            with open(f"categorized_lines.txt", 'a') as file:
                                file.write(f"{line.strip()} - {bucket_file}\n")
                            break
                        
                    if found:
                        break

                    else:
                        # Look for the exact match of the processed line in the bucket file
                        if line_processed == bucket_line:
                            found = True
                            with open(f"categorized_lines.txt", 'a') as file:
                                file.write(f"{line.strip()} - {bucket_file}\n")
                            break
                # If the processed line is not found in any bucket file, categorize as '[unknown] - cpu-cycle - application_logic'
                if not found:
                    with open("uncategorized.txt", 'a') as file:
                        if line.strip(): # Skip writing empty lines
                            file.write(line + '\n')
                   
    
def find_network_keywords():

    if os.path.exists('found_network_keywords.txt'):
        os.remove('found_network_keywords.txt')

    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    with open('found_network_keywords.txt', 'w') as file:
        write_next_line = False
        for line in lines:
            if 'network_keywords' in line:
                file.write(line)
                write_next_line = True
            elif write_next_line:
                file.write(line)
                write_next_line = False
           

    # Read the found_network_keywords.txt file 
    with open('found_network_keywords.txt', 'r') as file:
        lines = file.readlines()

        # Extract the first part of the line
        previous_branch_stack_num = None

        with open('processed_found_network_keywords.txt', 'w') as outfile:
            for line in lines:
                function_name = line.split('-')[0].strip()
                branch_stack_num = line.split('-')[3].strip()
                total_cpu_cycles_taken = int(line.split('-')[5].strip())
                category = line.split('-')[7].strip()


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


            