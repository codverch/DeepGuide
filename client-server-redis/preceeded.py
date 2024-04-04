import os
import matplotlib.pyplot as plt
import re 

if os.path.exists('found_network_keywords.txt'):
    os.remove('found_network_keywords.txt')
if os.path.exists('processed_found_network_keywords.txt'):
    os.remove('processed_found_network_keywords.txt')
if os.path.exists('categorized_lines.txt'):
    os.remove('categorized_lines.txt')
if os.path.exists('uncategorized.txt'):
    os.remove('uncategorized.txt')
if os.path.exists('network_category_followed_by_category.png'):
    os.remove('network_category_followed_by_category.png')
        
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
                        outfile.write(f"{from_function} - {idx} - {cpu_cycle}\n") # idx is branch_stack_number

                        # Open the extracted_from_functions.txt file in append mode
                        with open('extracted_from_functions.txt', 'a') as func_outfile:
                            # Write "from" function and branch stack number to the extracted functions file
                            func_outfile.write(f"{from_function} - {idx} - {cpu_cycle}\n") # idx is branch_stack_number

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
                    parts = line.split('-')
                    branch_stack_number = parts[1].strip()
                    cpu_cycle = parts[2].strip()
                        
                    with open(f"categorized_lines.txt", 'a') as file:
                        file.write(f"[unknown] - {branch_stack_number} - {cpu_cycle} - application_logic_keywords\n")
            else:
                # Split the line at the first space to exclude the CPU cycle value
                line_processed = line.split(' - ')[0] # Compare only the function name, however write the entire line
                # Check if this processed line is present in any of the bucket files as a substring
                found = False
                for bucket_file in bucket_files:
                    # Check if any keyword from the bucket file is a substring of the processed line
                    for bucket_line in bucket_file_contents[bucket_file]:
                        if bucket_line in line_processed: # If a line in the bucket file is found in the processed line (substring match)
                            found = True
                            with open(f"categorized_lines.txt", 'a') as file:
                                function_name = line.split(' - ')[0].strip()
                                branch_stack_number = line.split(' - ')[1].strip()
                                cpu_cycle = line.split(' - ')[2].strip()
                                category = os.path.basename(bucket_file).strip()
                                file.write(f"{function_name} - {branch_stack_number} - {cpu_cycle} - {category}\n")
                            break
                        
                    if found:
                        break

                    else:
                        # Look for the exact match of the processed line in the bucket file
                        if line_processed == bucket_line:
                            found = True
                            with open(f"categorized_lines.txt", 'a') as file:
                                function_name = line.split(' - ')[0].strip()
                                branch_stack_number = line.split(' - ')[1].strip()
                                cpu_cycle = line.split(' - ')[2].strip()
                                category = os.path.basename(bucket_file).strip()
                                file.write(f"{function_name} - {branch_stack_number} - {cpu_cycle} - {category}\n")
                            break
                # If the processed line is not found in any bucket file, categorize as '[unknown] - cpu-cycle - application_logic'
                if not found:
                    with open("uncategorized.txt", 'a') as file:
                        if line.strip(): # Skip writing empty lines
                            function_name = line.split(' - ')[0]
                            branch_stack_number = line.split(' - ')[1]
                            cpu_cycle = line.split(' - ')[2]
                            file.write(f"{function_name} - {branch_stack_number} - {cpu_cycle} - application_logic_keywords\n")
                   
    
process_file()
categorize_functions()

"""
This function reads lines from a file called 'categorized_lines.txt', identifies lines containing the string 'network_keywords', 
and writes them to a new file called 'found_network_keywords.txt'. For each identified line, it also writes
the next line to the output file.
"""

def find_network_keywords():

    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    with open('found_network_keywords.txt', 'w') as file:
        write_next_line = False
        for line in lines:
            if 'network_keywords' in line:
                function_name = line.split('-')[0].strip()
                branch_stack_num = line.split('-')[1].strip()
                cpu_cycle = line.split('-')[2].strip()
                category = line.split('-')[3].strip()
                file.write(f"{function_name} - {branch_stack_num} - {cpu_cycle} - {category}\n")
                write_next_line = True
            elif write_next_line:
                function_name = line.split('-')[0].strip()
                branch_stack_num = line.split('-')[1].strip()
                cpu_cycle = line.split('-')[2].strip()
                category = line.split('-')[3].strip()
                file.write(f"{function_name} - {branch_stack_num} - {cpu_cycle} - {category}\n")
                write_next_line = False

find_network_keywords()

"""
# Read and process lines from 'found_network_keywords.txt', aggregating CPU cycles for lines with the same branch stack number
# Write the aggregated data to 'processed_found_network_keywords.txt', including function name, total CPU cycles, and category
# Initialize variables to track the previous branch stack number, function name, total CPU cycles, and category
# Skip lines with insufficient parts and print a message, then continue processing the remaining lines
"""

def computation():
    # Read the 'found_network_keywords.txt' file
    with open('found_network_keywords.txt', 'r') as file:
        lines = file.readlines()

    # Extract the first part of the line
    previous_branch_stack_num = None

    with open('processed_found_network_keywords.txt', 'w') as outfile:
        for line in lines:
            parts = line.split('-')
            if len(parts) < 3:
                print(f"Skipping line: {line}")
                continue
            
            function_name = parts[0].strip()
            branch_stack_num = parts[1].strip()
            total_cpu_cycles_taken = int(parts[2].strip())
            category = parts[3].strip()

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

computation()

"""
Each line in the 'processed_found_network_keywords.txt' file follows a specific format:
  - One line consists of 'network_keywords' followed by another line containing a category that is not classified as a network category.
The objective is to visualize the percentage of CPU cycles attributed to the network category in conjunction with various other categories.
Goal is to observe CPU cycles taken by network + kernel, network + application_logic, network + unknown, and network + other categories.

This code block reads lines from 'processed_found_network_keywords.txt' and processes them in pairs, 
combining CPU cycle counts for network categories followed by other categories. 
It then calculates the percentage of CPU cycles for each combination and stores the results in
network_followed_by_category_cpu_percentages.
"""

"""
This function reads pairs of lines from a file, where each pair represents a network category 
followed by another category, and aggregates the CPU cycles for each pair. 
It then calculates the percentage of CPU cycles for each pair and plots the results as a bar chart,
with each bar representing a network category and different colors indicating the following 
category. The legend is moved outside the plot for clarity, and percentage values are displayed 
above the bars for easy comparison.
"""

def plot_network_category_combinations_cpu_cycles():
    with open('processed_found_network_keywords.txt', 'r') as file:
        lines = file.readlines()

    buckets = ['kernel_keywords', 
           'application_logic_keywords', 'c_libraries_keywords',
            'serialization_keywords', 
           'sync_keywords', 'miscellaneous_keywords', 'network_keywords',
           'compress_keywords', 'encryption_keywords', 'hash_keywords', 'mem_keywords'] # Add network_keywords since they probably don't belong to the same branch stack

    cpu_cycles = {"network_followed_by_" + bucket : 0 for bucket in buckets}

    # Read a line and its following line to process pairs
    # The first line is network and the second line is of a different category
    for i in range(0, len(lines), 2):
        network_category = lines[i].split('-')[3].strip()
        other_category = lines[i+1].split('-')[3].strip()
        cpu_cycles["network_followed_by_" + other_category] += int(lines[i].split('-')[2].strip())

    # Calculate the total CPU cycles for all categories in 'categorized_lines.txt'
    with open ('categorized_lines.txt', 'r') as file:
        lines = file.readlines()
        total_cpu_cycles_all_from_functions = 0
        for line in lines:
            total_cpu_cycles_all_from_functions += int(line.split('-')[2].strip())

    # Calculate the percentage of CPU cycles for each network category combination
    network_followed_by_category_cpu_percentages = {key: (value / total_cpu_cycles_all_from_functions) * 100 for key, value in cpu_cycles.items()}

    # Plot the percentage of CPU cycles for each network category combination
    plt.figure(figsize=(15, 10))
    plt.bar(network_followed_by_category_cpu_percentages.keys(), network_followed_by_category_cpu_percentages.values(), color='skyblue')
    plt.ylabel('Percentage of CPU Cycles (%)')
    plt.title('Percentage of CPU Cycles for Network Category Followed by Other Categories')
    plt.xticks(rotation=45)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    # Add the percentage values above the bars
    for key, value in network_followed_by_category_cpu_percentages.items():
        plt.text(key, value + 0.5, f'{value:.2f}%', ha='center')
    plt.tight_layout()
    plt.savefig('network_category_followed_by_category.png')
    plt.show()
       
plot_network_category_combinations_cpu_cycles()
