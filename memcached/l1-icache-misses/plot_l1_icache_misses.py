import re
import os
import matplotlib.pyplot as plt
from collections import defaultdict

def extract_to_addresses():
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

def plot_icache_misses():
    # Read the categorized_lines.txt file
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    # Dictionary to store the counts for each category
    category_counts = defaultdict(int)

    # Process each line to extract the category and increment the count
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) < 2:
            continue
        # Merge 'application_logic' and 'application_logic_keywords' into a single category
        category = parts[-1]
        if category in ['application_logic', 'application_logic_keywords']:
            category = 'application_logic'
        category_counts[category] += 1

    # Print the category and count
    for category, count in category_counts.items():
        print(f"{category}: {count}")

    # Plot the bar graph
    categories = list(category_counts.keys())
    counts = list(category_counts.values())
    plt.figure(figsize=(10, 6))
    plt.bar(categories, counts)
    plt.xlabel('Tax Categories')
    plt.ylabel('Count')
    plt.title('L1 Instruction Cache Misses by Tax Category')

    # Annotate the bars with their respective counts
    for i, count in enumerate(counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('icache_misses_by_category.png')
    plt.show()

def plot_application_vs_other_taxes():
    # Read the categorized_lines.txt file
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    # Dictionary to store the counts for each category
    category_counts = defaultdict(int)

    # Process each line to extract the category and increment the count
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) < 2:
            continue
        # Merge 'application_logic' and 'application_logic_keywords' into a single category
        category = parts[-1]
        if category in ['application_logic', 'application_logic_keywords']:
            category = 'application_logic'
        category_counts[category] += 1

    # Get the count for 'application_logic' and all other categories
    application_logic_count = category_counts['application_logic']
    other_taxes_count = sum(count for category, count in category_counts.items() if category != 'application_logic')

    # Plot the bar graph
    categories = ['Application Logic', 'Other Taxes']
    counts = [application_logic_count, other_taxes_count]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, counts)
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('L1 Instruction Cache Misses: Application Logic vs Other Taxes')

    # Annotate the bars with their respective counts
    for i, count in enumerate(counts):
        plt.text(i, count, str(count), ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('application_vs_other_taxes.png')
    plt.show()

def plot_icache_misses_percentage():
    # Read the categorized_lines.txt file
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    # Dictionary to store the counts for each category
    category_counts = defaultdict(int)

    # Process each line to extract the category and increment the count
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) < 2:
            continue
        # Merge 'application_logic' and 'application_logic_keywords' into a single category
        category = parts[-1]
        if category in ['application_logic', 'application_logic_keywords']:
            category = 'application_logic'
        category_counts[category] += 1

    # Calculate the total number of icache misses
    total_ic_misses = sum(category_counts.values())

    # Calculate the percentage of icache misses for each category
    percentage_by_category = {category: (count / total_ic_misses) * 100 for category, count in category_counts.items()}

    # Print the percentage for each category
    for category, percentage in percentage_by_category.items():
        print(f"{category}: {percentage:.2f}%")

    # Plot the bar graph
    categories = list(percentage_by_category.keys())
    percentages = list(percentage_by_category.values())
    plt.figure(figsize=(10, 6))
    plt.bar(categories, percentages)
    plt.xlabel('Tax Categories')
    plt.ylabel('Percentage')
    plt.title('Percentage of L1 Instruction Cache Misses by Tax Category')

    # Annotate the bars with their respective percentages
    for i, percentage in enumerate(percentages):
        plt.text(i, percentage, f"{percentage:.2f}%", ha='center', va='bottom')

    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig('icache_misses_percentage_by_category.png')
    plt.show()

def plot_application_vs_other_taxes_percentage():
    # Read the categorized_lines.txt file
    with open('categorized_lines.txt', 'r') as file:
        lines = file.readlines()

    # Dictionary to store the counts for each category
    category_counts = defaultdict(int)

    # Process each line to extract the category and increment the count
    for line in lines:
        parts = line.strip().split(' - ')
        if len(parts) < 2:
            continue
        # Merge 'application_logic' and 'application_logic_keywords' into a single category
        category = parts[-1]
        if category in ['application_logic', 'application_logic_keywords']:
            category = 'application_logic'
        category_counts[category] += 1

    # Calculate the total number of icache misses
    total_ic_misses = sum(category_counts.values())

    # Calculate the percentage of icache misses for 'application_logic' and 'other_taxes'
    application_logic_percentage = (category_counts['application_logic'] / total_ic_misses) * 100
    other_taxes_percentage = (category_counts['miscellaneous_keywords'] + category_counts['kernel_keywords'] + 
                              category_counts['sync_keywords'] + category_counts['c_libraries_keywords']) / total_ic_misses * 100

    # Print the percentages
    print(f"Application Logic: {application_logic_percentage:.2f}%")
    print(f"Other Taxes: {other_taxes_percentage:.2f}%")

    # Plot the bar graph
    categories = ['Application Logic', 'Other Taxes']
    percentages = [application_logic_percentage, other_taxes_percentage]

    plt.figure(figsize=(8, 6))
    plt.bar(categories, percentages)
    plt.xlabel('Category')
    plt.ylabel('Percentage')
    plt.title('Percentage of L1 Instruction Cache Misses: Application Logic vs Other Taxes')

    # Annotate the bars with their respective percentages
    for i, percentage in enumerate(percentages):
        plt.text(i, percentage, f"{percentage:.2f}%", ha='center', va='bottom')

    plt.tight_layout()
    plt.savefig('application_vs_other_taxes_percentage.png')
    plt.show()


# Call the function to extract "To" addresses
extract_to_addresses()

# Call the function to categorize the lines
bucketize_lines()

# Call the function to plot the graph and save it as a PNG image
plot_icache_misses()

# Call the function to plot the graph and save it as a PNG image
plot_application_vs_other_taxes()

# Call the function to plot the percentage graph and save it as a PNG image
plot_icache_misses_percentage()

# Call the function to plot the percentage graph and save it as a PNG image
plot_application_vs_other_taxes_percentage()






