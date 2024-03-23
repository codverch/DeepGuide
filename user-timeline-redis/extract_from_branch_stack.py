
import re
import os
import matplotlib.pyplot as plt

# ===========================================================================================================================
# This function reads the 'branch_stack.txt' file, processes each line, and writes the result to 'processed_branch_stack.txt'.
# It removes empty lines and extracts function names from lines that do not start with '['.
# Lines starting with '[' are considered unknown functions. 
# Additionally, also writes the CPU cycle value of each function to the file.
# ===========================================================================================================================

def process_file():
    with open('branch_stack.txt', 'r') as file:
        lines = file.readlines()

    # Remove file named 'processed_branch_stack.txt' if it already exists
    if os.path.exists('processed_branch_stack.txt'):
        os.remove('processed_branch_stack.txt')
    if os.path.exists('categorized_lines.txt'):
        os.remove('categorized_lines.txt')
    if os.path.exists('uncategorized.txt'):
        os.remove('uncategorized.txt')

    with open('processed_branch_stack.txt', 'w') as outfile:
        for line in lines:
            # Skip empty lines
            if not line.strip():
                continue

            # Split the line into individual function calls
            segments = line.strip().split()

            # Process each segment to find "from" functions and their CPU cycles
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
                        outfile.write(f"{from_function} - {cpu_cycle}\n")


# ===========================================================================================================================

# ===========================================================================================================================
#   This function reads the 'processed_branch_stack.txt' file and categorizes each line based on keywords in the bucket files located in the 'bucketization' folder.
#   It categorizes lines into predefined categories such as 'application_logic', 'c_libraries', 'compress', etc., or as 'uncategorized' if no matching keyword is found.
#   The categorized lines are then written to 'categorized_lines.txt', and the uncategorized lines are written to 'uncategorized_lines.txt'.
# ===========================================================================================================================

def bucketize_lines():
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
                    else:
                        cpu_cycle = "unknown"
                    with open(f"categorized_lines.txt", 'a') as file:
                        file.write(f"[unknown] - {cpu_cycle} - application_logic_keywords\n")
            else:
                # Split the line at the first space to exclude the CPU cycle value
                line_processed = line.split(" ", 1)[0]
                # Check if this processed line is present in any of the bucket files
                found = False
                for bucket_file in bucket_files:
                    # Check if the processed line is in the processed bucket file content
                    if line_processed in bucket_file_contents[bucket_file]:
                        found = True
                        with open(f"categorized_lines.txt", 'a') as file:
                            file.write(f"{line.strip()} - {bucket_file}\n")
                        break
                # If the processed line is not found in any bucket file, categorize as '[unknown] - cpu-cycle - application_logic'
                if not found:
                     with open("uncategorized.txt", 'a') as file:
                        if line.strip(): # Skip writing empty lines
                            file.write(line + '\n')
                    
                   
# ===========================================================================================================================

def plot_app_logic_vs_orchestration():
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
    plt.title('CPU Cycle Usage: Application Logic vs Orchestration Work')

    # Add annotations on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')

    plt.savefig('app_logic_vs_orchestration.png')
    plt.close()

# ===========================================================================================================================

def plot_tax_breakdown():
    categories = {}

    with open('categorized_lines.txt', 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if len(parts) > 2:
                category = parts[-1].strip()  # The category name is the last part
                cpu_cycle = parts[1].strip()  # The CPU cycle is the second part
                if cpu_cycle.isdigit():
                    cpu_cycle = int(cpu_cycle)
                    if category not in categories:
                        categories[category] = cpu_cycle
                    else:
                        categories[category] += cpu_cycle  # Correctly increment the CPU cycle count

    # Calculate the total number of CPU cycles across all categories
    total_cycles = sum(categories.values())

    # Calculate the percentage of CPU cycles for each category
    percentages = {k: (v / total_cycles) * 100 for k, v in categories.items()}

    # Sort categories by their percentage for better visualization
    sorted_categories = dict(sorted(percentages.items(), key=lambda item: item[1], reverse=True))

    # Plotting
    plt.figure(figsize=(12, 8))
    bars = plt.bar(sorted_categories.keys(), sorted_categories.values(), color='blue')
    plt.xlabel('Categories')
    plt.ylabel('Percentage of CPU Cycles')
    plt.title('CPU Cycle Usage: Tax Breakdown')
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()  # Adjust layout to make room for the rotated x-axis labels

    # Add annotations on top of each bar
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')

    plt.savefig('tax_breakdown.png')  # Save as PDF
    plt.close()

# Call the function to process the file
process_file()
# Call the function to bucketize the lines
bucketize_lines()
# Call the function to plot the CPU cycle usage
plot_app_logic_vs_orchestration()
# Call the function to plot the tax breakdown
plot_tax_breakdown()