import matplotlib.pyplot as plt
from collections import defaultdict
import os
import re


def process_file():
    with open('branch_stack.txt', 'r') as file:
        lines = file.readlines()[:900] # Read only the first 10 lines

    files_to_remove = [
        'processed_branch_stack_preceeded.txt',
        'extracted_from_functions.txt',
        'categorized_lines_preceeded.txt',
        'uncategorized_preceeded.txt',
        'network_keywords_preceeded.txt',
        'network_keywords_succeeded.txt',
        'preceded_graph.png',
       'network_keywords_preceeded_final.txt',
        'succeeded_graph.png'
    ]

    for file_name in files_to_remove:
        if os.path.exists(file_name):
            os.remove(file_name)

    with open('processed_branch_stack_preceeded.txt', 'w') as outfile:
        for idx, line in enumerate(lines, start=1):  # Enumerate the lines to get the branch stack number
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

    # Read each line in the extracted_from_functions file and categorize it based on bucketization files
    with open('extracted_from_functions.txt', 'r') as infile:
        for line in infile:
            # Extract the function name, branch stack number, and CPU cycles from the line
            parts = line.split(' - ')
            function_name = parts[0].strip()
            branch_stack_number = parts[1].strip()
            cpu_cycles = parts[2].strip() if len(parts) > 2 else ''

            # Check if the function name is in any of the bucketization files
            if function_name.startswith("["):
                if function_name.startswith("[unknown]"):
                    # Categorize as application logic
                    with open('categorized_lines_preceeded.txt', 'a') as outfile:
                        outfile.write(f"{function_name} - {branch_stack_number} - {cpu_cycles} - application_logic_keywords\n")
            else:
                # Check if this processed line is present in any of the bucket files
                found = False
                for bucket_file in bucket_files:
                    # Check if the processed line is in the processed bucket file content
                    if function_name in bucket_file_contents[bucket_file]:
                        found = True
                        with open(f"categorized_lines_preceeded.txt", 'a') as file:
                            file.write(f"{function_name} - {branch_stack_number} - {cpu_cycles} - {bucket_file}\n")
                        break
                # If the processed line is not found in any bucket file, categorize as uncatagorized
                if not found:
                    with open("uncategorized_preceeded.txt", 'w') as file:
                        if line.strip(): # Skip writing empty lines
                            file.write(line + '\n')

    
def group_network_keywords():
    # Read each line in categorized_lines_preceeded.txt and group consecutive lines with network keywords from the same branch stack
    # as one entry and use the function name of the first line in the consecutive line sequence and the cpu cycle as the sum of the cpu cycles of all the lines in the sequence
    with open('categorized_lines_preceeded.txt', 'r') as file:
        lines = file.readlines()
        
    network_keywords_sequence = [] # A list to store the network keywords sequence
    previous_branch_stack_number = None
    previous_category = None
    total_cpu_cycles_of_sequence = 0

    for line in lines:
        parts = line.

# Redis is supposed to act as a server - setup it up - standalone application (redis) - workload generator 
# Goal - create a benchmark 
# grpc - look at example in the documentation - client-server (echo server - listening to requests and sends them back)

def plot_preceded_graph():
    with open('network_keywords_preceeded_final.txt', 'r') as file:
        lines = file.readlines()
        categories = defaultdict(int)
        for line in lines:
            _, category = line.split(' - ')
            categories[category.strip()] += 1

        plt.figure(figsize=(12, 6))
        bars = plt.bar(categories.keys(), categories.values())
        plt.xlabel('Category')
        plt.ylabel('Count')
        plt.title('Functions Preceded by Network Keywords')
        plt.xticks(rotation=45, ha='right')
        for bar in bars:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height + 0.5, str(int(height)), ha='center', va='bottom')
        plt.tight_layout()
        plt.savefig('preceded_graph.png')
        plt.show()


# Call the functions
process_file()
categorize_functions()
# identify_network_keywords_preceded()
group_network_keywords()
# plot_preceded_graph()


    



# Function to read the categorized lines and what keywords are network keywords preceeded by and create a plot


