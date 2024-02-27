import re
import os


def extract_function_and_misses():
    with open('branch_stack_merged.txt', 'r') as file1, open('branch_stack.txt', 'r') as file2:
        # Read all lines from branch_stack.txt
        functions = [line.strip() for line in file2.readlines()]

        with open('categorize_these.txt', 'w') as output_file:
            # Iterate over each line in branch_stack_merged.txt
            for line1 in file1:
                # Use regular expression to find the L1-icache-load-misses value
                match = re.search(r'\d+ L1-icache-load-misses:', line1)
                if match:
                    # Extract the value
                    value = match.group().split()[0]

                    # Check if there are any functions left in the list from branch_stack.txt
                    if functions:
                        # Pop the first function from the list and split by '/'
                        function_parts = functions.pop(0).split('/')
                        if len(function_parts) > 1:
                            function = function_parts[1].split('+')[0]
                            # Print the function name and the L1-icache-load-misses value on the same line
                            # print(f"{function} - {value}")
                            # Write the function name and the L1-icache-load-misses value to the output file
                            output_file.write(f"{function} - {value}\n")
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

    # Read the functions from categorize_these.txt and categorize them
    with open('categorize_these.txt', 'r') as file:
        functions = file.readlines()

    # Categorize each function
    categorized_functions = []
    for function in functions:
        # Extract the function name
        function_name = function.split(" - ")[0].strip()
        # Check if this function is present in any of the bucket files
        found = False
        for bucket_file in bucket_files:
            # Check if the function name is in the processed bucket file content
            if function_name in bucket_file_contents[bucket_file]:
                found = True
                categorized_functions.append(f"{function.strip()} - {bucket_file}")
                break
        # If the function is not found in any bucket file and starts with '[unknown]', categorize as 'application_logic'
        if not found and function_name.startswith('[unknown]'):
            categorized_functions.append(f"{function.strip()} - application_logic")

    # Write the categorized functions to a new file
    with open('categorized_functions.txt', 'w') as file:
        for line in categorized_functions:
            file.write(f"{line}\n")


# Call the function to categorize functions
categorize_functions()


# Call the function to extract the function name and L1-icache-load-misses
extract_function_and_misses()

# Call the function to categorize functions
categorize_functions()



# Call the function to categorize functions
categorize_functions()

