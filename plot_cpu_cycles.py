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

# Calculate total cycles
total_cycles = sum(tax_categories_cycles.values())

# Calculate percentages for each tax category
tax_categories_percentages = {category: (cycles / total_cycles) * 100 for category, cycles in tax_categories_cycles.items()}

# Plotting the bar graph for tax categories percentages
plt.figure(figsize=(15, 6))
plt.bar(tax_categories_percentages.keys(), tax_categories_percentages.values(), color='maroon')
plt.xlabel('Tax Category')
plt.ylabel('Percentage of CPU Cycles (%)')
plt.title('Percentage of CPU Cycles by Tax Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('cpu_cycles_percentage.png')
plt.close()

# Calculate percentage breakdown for Application Logic vs Other Tax Categories
application_logic_cycles = tax_categories_cycles['application_logic_keywords']
other_tax_categories_cycles = total_cycles - application_logic_cycles
percentages = [application_logic_cycles / total_cycles * 100, other_tax_categories_cycles / total_cycles * 100]

# Plotting the bar graph for Application Logic vs Other Tax Categories
plt.figure(figsize=(6, 6))
plt.bar(['Application Logic', 'Other Tax Categories'], percentages, color=['blue', 'orange'])
plt.xlabel('Category')
plt.ylabel('Percentage of CPU Cycles (%)')
plt.title('Percentage of CPU Cycles: Application Logic vs Other Tax Categories')
plt.tight_layout()
plt.savefig('cpu_cycles_application_logic_vs_other.png')
plt.close()

# Plotting the bar graph for raw CPU cycles tax breakdown
plt.figure(figsize=(15, 6))
plt.bar(tax_categories_cycles.keys(), tax_categories_cycles.values(), color='maroon')
plt.xlabel('Tax Category')
plt.ylabel('CPU Cycles')
plt.title('CPU Cycles by Tax Category')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('cpu_cycles_raw.png')
plt.close()

# Plotting the bar graph for raw CPU cycles of Application Logic vs Other Tax Categories
plt.figure(figsize=(6, 6))
plt.bar(['Application Logic', 'Other Tax Categories'], [application_logic_cycles, other_tax_categories_cycles], color=['blue', 'orange'])
plt.xlabel('Category')
plt.ylabel('CPU Cycles')
plt.title('CPU Cycles: Application Logic vs Other Tax Categories')
plt.tight_layout()
plt.savefig('cpu_cycles_application_logic_vs_other_raw.png')
plt.close()
