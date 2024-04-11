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

if os.path.exists('found_preceding_network_keywords.txt'):
    os.remove('found_preceding_network_keywords.txt')
        
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


def find_preceding_network_keywords():
    """
    Read all the lines from the categorized_lines.txt file.
    Whenever a line has the category 'network_keywords', write the previous line to the found_preceding_network_keywords.txt file.
    Do not write the same line twice.
    """
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    with open('found_preceding_network_keywords.txt', 'w') as outfile:
        i = 0
        while i < len(lines):
            if 'network_keywords' in lines[i]:
                # Write the previous line only if it's not a 'network_keywords' line
                if i - 1 >= 0 and 'network_keywords' not in lines[i - 1]:
                    outfile.write(lines[i - 1])
                # Write current line and any consecutive lines with 'network_keywords'
                while i < len(lines) and 'network_keywords' in lines[i]:
                    outfile.write(lines[i])
                    i += 1
            else:
                i += 1  # Move to the next line

find_preceding_network_keywords()

def process_found_network_keywords():
    """
    Read all the lines from the found_preceding_network_keywords.txt file.
    If there are consecutive lines with category 'network_keywords', write only the first function name to the found_network_keywords.txt file
    and sum their CPU cycles, if they belong to the same branch stack number.
    """
    with open('found_preceding_network_keywords.txt', 'r') as file:
        lines = file.readlines()

    with open('processed_found_network_keywords.txt', 'w') as outfile:
        i = 0
        while i < len(lines):
            if 'network_keywords' in lines[i]:
                # Write the first function name and sum the CPU cycles of consecutive lines with 'network_keywords'
                first_line = lines[i].split(' - ')
                cpu_cycles = int(first_line[2])
                i += 1
                while i < len(lines) and 'network_keywords' in lines[i]:
                    cpu_cycles += int(lines[i].split(' - ')[2])
                    i += 1
                outfile.write(f"{first_line[0]} - {first_line[1]} - {cpu_cycles} - network_keywords\n")
            else:
                # Write other lines as-is
                outfile.write(lines[i])
                i += 1  # Move to the next line

process_found_network_keywords()

def plot_category_network_combinations_cpu_cycles():
    """
    Process the input file to calculate the CPU cycles for each category combined with the network keyword,
    excluding cases where a network keyword is followed by another network keyword from a different branch stack.
    Plot the distribution and save the plot as 'category_network_combination.png'.
    """
    with open('processed_found_network_keywords.txt', 'r') as file:
        lines = file.readlines()

    buckets = ['kernel_keywords', 
           'application_logic_keywords', 'c_libraries_keywords',
           'serialization_keywords', 
           'sync_keywords', 'miscellaneous_keywords', 
           'compress_keywords', 'encryption_keywords', 'hash_keywords', 'mem_keywords']

    cpu_cycles = {bucket + "_followed_by_network": 0 for bucket in buckets}

    i = 0
    while i < len(lines) - 1:
        current_line_parts = lines[i].split(' - ')
        next_line_parts = lines[i + 1].split(' - ')
        if current_line_parts[3].strip() in buckets and next_line_parts[3].strip() == 'network_keywords' and current_line_parts[1] == next_line_parts[1]:
            cpu_cycles[current_line_parts[3].strip() + "_followed_by_network"] += int(next_line_parts[2].strip())
        i += 2

    total_cpu_cycles = sum(cpu_cycles.values())
    category_network_combination_cpu_percentages = {key: (value / total_cpu_cycles) * 100 for key, value in cpu_cycles.items()}

    plt.figure(figsize=(15, 10))
    keys = list(category_network_combination_cpu_percentages.keys())
    plt.bar(range(len(keys)), category_network_combination_cpu_percentages.values(), color='skyblue')
    plt.ylabel('Normalized Percentage of CPU Cycles (%)', fontsize=17)
    plt.title('Percentage of CPU Cycle Distribution for Category + Network Combination', fontsize=17)

    plt.xticks(range(len(keys)), [key.replace('_followed_by_network', '') + " + Network" for key in keys], rotation=50, fontsize=15, ha='right')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for i, value in enumerate(category_network_combination_cpu_percentages.values()):
        plt.text(i, value - -0.1, f'{value:.2f}%', ha='center', fontsize=15)
    plt.tight_layout()
    plt.savefig('category_network_combination.png')
    plt.show()

plot_category_network_combinations_cpu_cycles()




