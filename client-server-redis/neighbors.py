import os
import matplotlib.pyplot as plt
import re 

def process_file():
        with open('branch_stack.txt') as file:
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
                   

 # Check if 'categorized_lines.txt' exists, if it doesn't proceed to the next step
 # Otherwise, skip the file processing
if not os.path.exists('categorized_lines.txt'):
    process_file()
    categorize_functions()

def find_network_keywords():
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    with open('found_network_combined_with_serialization.txt', 'w') as outfile:
        for line in lines:
            # If there is network or serialization keyword in the line, write it to the output file
            if 'network' in line or 'serialization' in line:
                outfile.write(line)

find_network_keywords()

def computation():
    # Read the 'found_network_keywords.txt' file
    with open('found_network_keywords.txt', 'r') as file:
        lines = file.readlines()

    # Extract the first part of the line
    previous_branch_stack_num = None
    cumulative_cpu_cycles = 0
    first_function_name = None
    in_sequence = False

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
                cumulative_cpu_cycles += total_cpu_cycles_taken
                first_function_name = function_name
                in_sequence = category in ['network_keywords', 'serialization_keywords']
                continue

            # Check if branch stack num is the same as previous
            if branch_stack_num == previous_branch_stack_num:
                # Check if the category is network or serialization
                if category in ['network_keywords', 'serialization_keywords'] and in_sequence:
                    cumulative_cpu_cycles += total_cpu_cycles_taken
                else:
                    # Write the previous entry to the output file
                    outfile.write(f"{previous_branch_stack_num} - {first_function_name} - {cumulative_cpu_cycles} - {category}\n")
                    # Reset variables for the new chain with current values
                    cumulative_cpu_cycles = total_cpu_cycles_taken
                    first_function_name = function_name
                    in_sequence = category in ['network_keywords', 'serialization_keywords']
            else:
                # Write the previous entry to the output file
                outfile.write(f"{previous_branch_stack_num} - {first_function_name} - {cumulative_cpu_cycles} - {category}\n")
                # Reset variables for the new chain with current values
                cumulative_cpu_cycles = total_cpu_cycles_taken
                first_function_name = function_name
                in_sequence = category in ['network_keywords', 'serialization_keywords']
                previous_branch_stack_num = branch_stack_num

        # Write the last entry to the output file
        outfile.write(f"{previous_branch_stack_num} - {first_function_name} - {cumulative_cpu_cycles} - {category}\n")

computation()

def plot_network_category_combinations_cpu_cycles():
    with open('processed_found_network_keywords.txt', 'r') as file:
        lines = file.readlines()

    cpu_cycles = {"category_preceeded_by_network": 0}

    # Calculate the total CPU cycles for all categories in 'categorized_lines.txt'
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()
        total_cpu_cycles_all_from_functions = 0
        for line in lines:
            total_cpu_cycles_all_from_functions += int(line.split('-')[2].strip())

    # Calculate the percentage of CPU cycles for category + network combination
    for line in lines:
        parts = line.split('-')
        if len(parts) < 3:
            continue
        category = parts[3].strip()
        if category == "network_keywords":
            cpu_cycles["category_preceeded_by_network"] += int(parts[2].strip())

    # Normalize CPU cycles by the total CPU cycles

    if total_cpu_cycles_all_from_functions != 0:
        cpu_cycles_percentage = (cpu_cycles["category_preceeded_by_network"] / total_cpu_cycles_all_from_functions) * 100
    else:
        cpu_cycles_percentage = 0

    # Plot the percentage of CPU cycles for category + network combination
    plt.figure(figsize=(10, 6))
    plt.bar(["Category Preceeded by Network"], [cpu_cycles_percentage], color='limegreen')
    plt.ylabel('Normalized Percentage of CPU Cycles (%)', fontsize=14)
    plt.title('Percentage of CPU Cycles for Category Preceeded by Network', fontsize=16)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.text(0, cpu_cycles_percentage - 2, f'{cpu_cycles_percentage:.2f}%', ha='center', fontsize=14)
    plt.tight_layout()
    plt.savefig('category_preceeded_by_network.png')
    plt.show()

plot_network_category_combinations_cpu_cycles()
