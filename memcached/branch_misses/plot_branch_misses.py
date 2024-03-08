import re
import os
import matplotlib.pyplot as plt

# Clean up previous files 
if os.path.exists('processed_branch_stack.txt'):
    os.remove('processed_branch_stack.txt')
if os.path.exists('categorized_lines.txt'):
    os.remove('categorized_lines.txt')
if os.path.exists('uncategorized.txt'):
    os.remove('uncategorized.txt')
if os.path.exists('categorized_lines_plot.png'):
    os.remove('categorized_lines_plot.png')
if os.path.exists('branch_misses_percentage.png'):
    os.remove('branch_misses_percentage.png')

# Read branch_misses.txt
with open("branch_misses.txt", 'r') as file:
    lines = file.readlines() # Contains the branch_stacks of the branch-misses 

# Extract the function names of the "To" functions from the branch_stacks if a line is empty then write the empty line as is to the file - processed_branch_stack.txt
with open('processed_branch_stack.txt', 'w') as outfile:
    for line in lines:
        if not line.strip():
            outfile.write('\n') # Write the empty line as is to the file
            continue
        match = re.search(r'/([\w.@]+)\+0x\w+/(M|P)/', line)
        if match:
            outfile.write(match.group(1) + '\n')

# ===========================================================================================================================

# Function to categorize the function names in processed_branch_stack.txt and write to "categorized_lines.txt" and "uncategorized_lines.txt"


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
            # If line is empty, categorize as no_branch_stack
            if line.strip() == "":
                with open(f"categorized_lines.txt", 'a') as file:
                    file.write(f"no_branch_stack\n")
            else:
                # Check if this processed line is present in any of the bucket files
                found = False
                for bucket_file in bucket_files:
                    # Check if the processed line is in the processed bucket file content
                    if any(keyword in line for keyword in bucket_file_contents[bucket_file]):
                        found = True
                        with open(f"categorized_lines.txt", 'a') as file:
                            file.write(f"{line.strip()} - {bucket_file}\n")
                        break
                # If the processed line is not found in any bucket file, categorize as '[unknown] - cpu-cycle - application_logic'
                if not found:
                     with open("uncategorized.txt", 'a') as file:
                        if line.strip(): # Skip writing empty lines
                            file.write(line + '\n')

def plot_categorized_lines(file_path):
    # Read the file and categorize each line
    categories = {}
    total_count = 0
    with open(file_path, 'r') as file:
        for line in file:
            parts = line.strip().split(' - ')
            if parts[0] == 'no_branch_stack':
                category = 'no_branch_stack'
            else:
                category = parts[1]
            if category in categories:
                categories[category] += 1
            else:
                categories[category] = 1
            total_count += 1
    
    # Plot the categorized data as a bar graph
    plt.figure(figsize=(12, 6))
    bars = plt.bar(categories.keys(), categories.values(), color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Count')
    plt.title('Categorized Lines')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height}', ha='center', va='bottom')
    
    # Save the plot as an image
    plt.savefig('categorized_lines_plot.png')
    plt.show()

    # Plot the percentage of branch misses
    plt.figure(figsize=(12, 6))
    percentages = {category: (count / total_count) * 100 for category, count in categories.items()}
    bars = plt.bar(percentages.keys(), percentages.values(), color='skyblue')
    plt.xlabel('Category')
    plt.ylabel('Percentage')
    plt.title('Percentage of Branch Misses')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.2f}%', ha='center', va='bottom')
    
    # Save the plot as an image
    plt.savefig('branch_misses_percentage.png')
    plt.show()

# Specify the path to your categorized_lines.txt file
file_path = 'categorized_lines.txt'

# ===========================================================================================================================
bucketize_lines()
plot_categorized_lines(file_path)