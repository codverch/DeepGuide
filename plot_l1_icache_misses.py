import matplotlib.pyplot as plt
from collections import defaultdict

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

# Call the function to plot the graph and save it as a PNG image
plot_icache_misses()
