
import re
import os

# ===========================================================================================================================
# This function reads the 'branch_stack.txt' file, processes each line, and writes the result to 'processed_branch_stack.txt'.
# It removes empty lines and extracts function names from lines that do not start with '['.
# Lines starting with '[' are considered unknown functions. 
# Additionally, also writes the CPU cycle value of each function to the file.
# ===========================================================================================================================

def process_file():
    with open('branch_stack.txt', 'r') as file:
        lines = file.readlines()

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
                        file.write(f"[unknown] - {cpu_cycle} - application_logic\n")
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

# Call the function to process the file
process_file()
# Call the function to bucketize the lines
bucketize_lines()
