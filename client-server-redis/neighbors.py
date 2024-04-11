import os
import matplotlib.pyplot as plt
import re 

if os.path.exists('processed_found_network_keywords.txt'):
    os.remove('processed_found_network_keywords.txt')
if os.path.exists('category_surrounded_by_network.png'):
    os.remove('category_surrounded_by_network.png')

if os.path.exists('found_network_and_serialization_keywords.txt'):
    os.remove('found_network_and_serialization_keywords.txt')

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
                   
process_file()
categorize_functions()


def find_network_and_serialization_keywords():
    # Open the input file for reading
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()  # Read all lines into a list

    # Open a new file for writing the found sequences
    with open('found_network_and_serialization_keywords.txt', 'w') as file:
        i = 0
        # Iterate over the lines in the file
        while i < len(lines) - 1:
            current_line = lines[i]  # Get the current line
            next_line = lines[i + 1]  # Get the next line

            # Check if the current line or the next line contains 'network_keywords' or 'serialization_keywords'
            if 'network_keywords' in current_line or 'serialization_keywords' in current_line or 'network_keywords' in next_line or 'serialization_keywords' in next_line:
                network_sequence = []  # Initialize a list to store the network sequence
                j = i  # Start searching from the current line
                while j < len(lines) - 1:
                    current_line = lines[j]  # Get the current line in the loop
                    next_line = lines[j + 1]  # Get the next line in the loop
                    current_branch_stack = current_line.split('-')[1].strip()
                    next_branch_stack = next_line.split('-')[1].strip()

                    # Check if the current line contains 'network_keywords' or 'serialization_keywords' and has the same branch stack as the next line
                    if ('network_keywords' in current_line or 'serialization_keywords' in current_line) and current_branch_stack == next_branch_stack:
                        # Add the line to the network sequence
                        network_sequence.append(current_line)
                    else:
                        # Check if the network sequence contains both keywords
                        if any('network_keywords' in line for line in network_sequence) and any('serialization_keywords' in line for line in network_sequence):
                            # Write the sequence to the file if it contains both keywords
                            for line in network_sequence:
                                file.write(line)
                            file.write(next_line)  # Write the next line as it contains the opposite keyword
                            break  # Exit the loop
                        else:
                            break  # Exit the loop if the sequence doesn't contain both keywords
                    j += 1  # Move to the next line
                i = j + 1  # Update the outer loop index to continue from where the inner loop ended
            else:
                i += 1  # Move to the next line if neither the current nor the next line contains the keywords

                    
find_network_and_serialization_keywords()


def plot_cpu_cycles():
    with open('found_network_and_serialization_keywords.txt', 'r') as file:
        lines = file.readlines()

    # Compute the sum of CPU cycles for each function
    cpu_cycles = 0
    for line in lines:
        cpu_cycles += int(line.split('-')[2].strip())
  
    # Calculate the total CPU cycles for all categories in 'categorized_lines.txt'
    with open ('categorized_lines.txt', 'r') as file:
        lines = file.readlines()
        total_cpu_cycles_all_from_functions = 0
        for line in lines:
            total_cpu_cycles_all_from_functions += int(line.split('-')[2].strip())
    
    # Normalized percentage of CPU cycles for functions with network and serialization keywords
    total_cpu_cycles_network_serialization_percentage = (cpu_cycles / total_cpu_cycles_all_from_functions) * 100

    # Plotting
    plt.figure(figsize=(15, 10))
    bar = plt.bar('Network + Serialization', total_cpu_cycles_network_serialization_percentage, color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('CPU Cycles (%)')
    plt.title('CPU Cycles for Functions with Network and Serialization Keywords')
    # Percentage of CPU cycles for functions with network and serialization keywords on the bar plot
    plt.text('Network + Serialization', total_cpu_cycles_network_serialization_percentage, f"{total_cpu_cycles_network_serialization_percentage:.2f}%", ha='center', va='bottom')
    plt.savefig('cpu_cycles_plot.png')
    plt.show()

# plot_cpu_cycles()
