import matplotlib.pyplot as plt
from collections import defaultdict

# Dictionary to store the CPU cycles for each tax category
tax_categories_cycles = defaultdict(int)

# Read the categorized_lines.txt file
with open('categorized_lines.txt', 'r') as file:
    lines = file.readlines()

    # Process each line
    for line in lines:
        # Split the line to extract the function name, CPU cycle, and tax category
        function_name, cycles, tax_category = line.split(' - ')

        # Add the CPU cycles to the corresponding tax category
        tax_categories_cycles[tax_category.strip()] += int(cycles)

# Total CPU cycles
total_cycles = sum(tax_categories_cycles.values())

# Calculate percentage of CPU cycles for each tax category
percentages = {category: (cycles / total_cycles) * 100 for category, cycles in tax_categories_cycles.items()}

# Print the values
print("CPU Cycles by Tax Category:")
for category, cycles in tax_categories_cycles.items():
    print(f"{category}: {cycles}")

print("\nPercentage of CPU Cycles by Tax Category:")
for category, percentage in percentages.items():
    print(f"{category}: {percentage:.2f}%")

# Plotting the bar graph for CPU cycles
plt.figure(figsize=(10, 6))
plt.bar(tax_categories_cycles.keys(), tax_categories_cycles.values(), color='maroon')
plt.xlabel('Tax Category')
plt.ylabel('CPU Cycles')
plt.title('CPU Cycles by Tax Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('cpu_cycles.png')
plt.show()

# Plotting the bar graph for percentage of CPU cycles
plt.figure(figsize=(10, 6))
plt.bar(percentages.keys(), percentages.values(), color='blue')
plt.xlabel('Tax Category')
plt.ylabel('Percentage of CPU Cycles')
plt.title('Percentage of CPU Cycles by Tax Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('cpu_cycles_percentage.png')
plt.show()
