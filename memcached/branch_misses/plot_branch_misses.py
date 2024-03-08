import re

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
