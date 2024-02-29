import re
import os

# Open the branch_stack.txt file for reading
with open("branch_stack.txt", "r") as file:
    # Read all lines from the file
    lines = file.readlines()

# Open the extracted_to_addresses.txt file for writing
with open("extracted_to_addresses.txt", "w") as file:
    # Initialize a counter for the total number of i-cache-misses
    total_ic_misses = 0
    # Loop through each line in the file
    for line in lines:
        # Remove leading and trailing whitespace from the line
        line = line.strip()
        # Check if the line is empty
        if not line:
            # Write a message indicating the line was empty
            file.write("This line was empty in the branch stack\n")
        else:
            # Split the line by "/" and extract the second function name
            functions = line.split("/")
            if len(functions) >= 2:
                to_address_parts = functions[1].split("+")
                to_address = to_address_parts[0]
                # Write the "To" address to the file
                file.write(to_address + "\n")
                # Increment the total number of i-cache-misses
                total_ic_misses += 1

# Print the total number of i-cache-misses
print("Total number of i-cache-misses:", total_ic_misses)

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
    
    # Categorize the lines in the 'extracted_to_addresses.txt' file
    with open('extracted_to_addresses.txt', 'r') as file:
        lines = file.readlines()
        for line in lines:
            # Remove leading and trailing whitespace from the line
            line = line.strip()
            # Skip lines that indicate empty lines
            if line == "This line was empty in the branch stack":
                continue
            # Check if the line starts with '[unknown]'
            if line.startswith("[unknown]"):
                with open(f"categorized_lines.txt", 'a') as file:
                    file.write(f"{line} - application_logic_keywords\n")
                continue
            # Check if this processed line is present in any of the bucket files
            found = False
            for bucket_file in bucket_files:
                # Check if the processed line is in the processed bucket file content
                if line in bucket_file_contents[bucket_file]:
                    found = True
                    with open(f"categorized_lines.txt", 'a') as file:
                        file.write(f"{line} - {bucket_file}\n")
                    break
            # If the processed line is not found in any bucket file, categorize as 'application_logic'
            if not found:
                with open(f"categorized_lines.txt", 'a') as file:
                    file.write(f"{line} - application_logic\n")

# Call the function to categorize the lines
bucketize_lines()


# Call the function to categorize the lines
bucketize_lines()
