import os
import matplotlib.pyplot as plt
import re 

files_to_remove = [
    'found_network_keywords.txt',
    'processed_found_network_keywords.txt',
    'categorized_lines.txt',
    'uncategorized.txt',
    'network_category_followed_by_category.png'
]

for file_name in files_to_remove:
    if os.path.exists(file_name):
        os.remove(file_name)

        
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
Read all the lines from the categorized_lines.txt file.
Whenever the category is 'network', write that line and the next line to the found_network_keywords.txt file.
Do not write the same line twice.
"""

def find_network_keywords():
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    with open('found_network_keywords.txt', 'w') as outfile:
        i = 0
        while i < len(lines):
            if 'network' in lines[i]:
                outfile.write(lines[i])
                if i + 1 < len(lines):  # Check if there is a next line
                    outfile.write(lines[i + 1])
                i += 2  # Skip the next line as it has already been written
            else:
                i += 1  # Move to the next line

find_network_keywords()

"""
Process the found_network_keywords.txt file to sum the CPU cycles taken by consecutive network keywords that 
belong to the same branch stack, and we take the function name of the first function in the sequence as the
function name. Write the processed data to the processed_found_network_keywords.txt file.
"""

def processed_found_network_keywords():
    """
    Process the lines in the 'found_network_keywords.txt' file.
    Combine consecutive lines with matching branch stack numbers and category 'network_keywords' by summing their CPU cycles.
    Write the processed lines to the 'processed_found_network_keywords.txt' file.
    """
    with open('found_network_keywords.txt', 'r') as file:
        lines = file.readlines()

    with open('processed_found_network_keywords.txt', 'w') as outfile:
        prev_line = None
        for line in lines:
            # Initialize prev_line if it's the first iteration
            if prev_line is None:
                prev_line = line
                continue

            prev_line_parts = prev_line.split(' - ')
            line_parts = line.split(' - ')

            # Check if both lines have four parts and belong to the same category
            if prev_line_parts[3].strip() == 'network_keywords' and line_parts[3].strip() == 'network_keywords':
                # If the branch stack number and category match, add CPU cycles and update prev_line
                if prev_line_parts[1] == line_parts[1]:
                    prev_cpu_cycle = int(prev_line_parts[2])
                    cpu_cycle = int(line_parts[2])
                    prev_cpu_cycle += cpu_cycle
                    prev_line = f"{prev_line_parts[0]} - {prev_line_parts[1]} - {prev_cpu_cycle} - network_keywords\n"
                else:
                    # If branch stack number changes, write prev_line to the output file
                    outfile.write(prev_line)
                    prev_line = line
            else:
                # If they don't have the same category, write both lines to the output file
                outfile.write(prev_line)
                prev_line = line
                
        # Write the last line if it exists
        if prev_line is not None:
            outfile.write(prev_line)

    """
    Explanation of the function:
    - It reads lines from 'found_network_keywords.txt'.
    - It combines consecutive lines with matching branch stack numbers and category 'network_keywords' by summing their CPU cycles.
    - If consecutive lines have different branch stack numbers or categories, it writes them to the 'processed_found_network_keywords.txt' file.
    """

processed_found_network_keywords()


def plot_category_network_combinations_cpu_cycles():
    """
    Process the 'processed_found_network_keywords.txt' file to calculate the percentage distribution of CPU cycles
    for each category combined with the network keyword, excluding cases where a network keyword is followed by another
    network keyword from a different branch stack. Plot the distribution and save the plot as
    'category_network_preceeded_by_network.png'.
    """
    with open('processed_found_network_keywords.txt', 'r') as file:
        lines = file.readlines()

    buckets = ['kernel_keywords', 
           'application_logic_keywords', 'c_libraries_keywords',
           'serialization_keywords', 
           'sync_keywords', 'miscellaneous_keywords', 
           'compress_keywords', 'encryption_keywords', 'hash_keywords', 'mem_keywords']


    cpu_cycles = {"network_followed_by_" + bucket : 0 for bucket in buckets}

    i = 0
    while i < len(lines) - 1:  # Ensure there is a next line to process
        prev_line_parts = lines[i].split(' - ')
        current_line_parts = lines[i + 1].split(' - ')
        if prev_line_parts[3].strip() == 'network_keywords' and current_line_parts[3].strip() != 'network_keywords' and prev_line_parts[1] == current_line_parts[1]:
            cpu_cycles["network_followed_by_" + current_line_parts[3].strip()] += int(prev_line_parts[2].strip())
            i += 2  # Skip the next line as it has already been processed
        else:
            i += 1  # Move to the next line

    total_cpu_cycles_all_from_functions = 0
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()
        total_cpu_cycles_all_from_functions = sum(int(line.split('-')[2].strip()) for line in lines)

    category_network_combination_cpu_percentages = {key: (value / total_cpu_cycles_all_from_functions) * 100 for key, value in cpu_cycles.items()}

    plt.figure(figsize=(15, 10))
    keys = list(category_network_combination_cpu_percentages.keys())
    plt.bar(range(len(keys)), category_network_combination_cpu_percentages.values(), color='limegreen')
    plt.ylabel('Normalized Percentage of CPU Cycles (%)', fontsize=17)
    plt.title('Percentage of CPU Cycle Distribution for Category + Network Combination', fontsize=17)

    name_mapping = {}
    for old_name in keys:
        # Split the old name into parts
        parts = old_name.split('_')

        # Find the index of 'network' in the parts list
        network_index = parts.index('network')

        # Keep 'network' and the part after 'network_followed_by_'
        kept_parts = [parts[network_index + 3]]

        # If the part after 'network' is 'c' or 'application logic', append ' Libraries' to it
        if kept_parts[0] == 'c':
            kept_parts[0] += ' Libraries'  
        elif kept_parts[0] == 'application':
            kept_parts[0] += ' Logic'

        # Join the parts back together, capitalizing each word
        new_name = ' + '.join(word.title() for word in kept_parts if word != 'keywords')
        # print(new_name)

        name_mapping[old_name] = new_name

        
    
    plt.xticks(range(len(keys)), ['Network + ' + name_mapping[key] for key in keys], rotation=50, fontsize=15, ha='right')

    plt.grid(axis='y', linestyle='--', alpha=0.7)
    for i, value in enumerate(category_network_combination_cpu_percentages.values()):
        plt.text(i, value - -0.1, f'{value:.2f}%', ha='center', fontsize=15)
    plt.tight_layout()
    plt.savefig('category_network_combination.png')
    plt.show()

plot_category_network_combinations_cpu_cycles()
