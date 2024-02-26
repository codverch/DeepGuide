
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
        # Read all lines from the file
        lines = file.readlines()

        with open('processed_branch_stack.txt', 'w') as file:
            # Process each line
            for line in lines:
                # Skip empty lines - These samples don't have branch stack
                if not line.strip():
                    continue
                # Process lines that do not start with '[' - These are unknown functions
                if not line.startswith("["):
                    # Find the index of '+' to extract function name
                    index = line.find('+')

                    if index != -1:
                        # Write the function name to the file
                        file.write(line[:index] + " -")

                        # Pattern to match the CPU cycle value
                        pattern = r'\/-\/-\/(\d+)'   
                        
                        # Code snippet to extract the CPU cycle value
                        functions = line.split()

                        # Iterate over each function in the line
                        for function in functions:
                            match = re.search(pattern, function) 
                            if match:
                                # Extract and write the CPU cycle value
                                cpu_cycle = match.group(1) # returns the first group of the match
                                # We only need the first match
                                file.write(" " + cpu_cycle + "\n") 
                                break

                    else:
                        file.write(line)
                # Write comment for lines starting with '['
                else:
                    pass

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
            # If the processed line is not found in any bucket file, write it to uncategorized
            if not found:
                with open(f"uncategorized_lines.txt", 'a') as file:
                    file.write(f"{line.strip()}\n")
# ===========================================================================================================================

# Call the function to process the file
process_file()
# Call the function to bucketize the lines
bucketize_lines()

