"""
DECISION TREE - Super Simple for Final Exam
Dataset: Play Outside (Weather + Temperature -> Play)
"""

import math

# Simple Dataset
data = [
    ['Sunny', 'Hot', 'No'],
    ['Sunny', 'Cool', 'Yes'],
    ['Rainy', 'Cool', 'No'],
    ['Rainy', 'Hot', 'No'],
    ['Cloudy', 'Hot', 'Yes'],
    ['Cloudy', 'Cool', 'Yes']
]

attributes = ['Weather', 'Temperature', 'Play']

# Calculate entropy
def entropy(rows):
    total = len(rows)
    counts = {}
    for row in rows:
        label = row[-1]  # Last column is target
        counts[label] = counts.get(label, 0) + 1
    
    ent = 0
    for count in counts.values():
        p = count / total
        ent -= p * math.log2(p)
    return ent

# Calculate information gain
def info_gain(rows, col):
    total_ent = entropy(rows)
    
    # Split data by column value
    splits = {}
    for row in rows:
        val = row[col]
        if val not in splits:
            splits[val] = []
        splits[val].append(row)
    
    # Calculate weighted entropy
    weighted = 0
    for subset in splits.values():
        weighted += (len(subset) / len(rows)) * entropy(subset)
    
    return total_ent - weighted

# Build tree
def build_tree(rows, attrs):
    labels = [row[-1] for row in rows]
    
    # If all same, return label
    if len(set(labels)) == 1:
        return labels[0]
    
    # If no attributes left, return most common
    if len(attrs) == 1:
        return max(set(labels), key=labels.count)
    
    # Find best attribute
    best_col = 0
    best_gain = 0
    for i in range(len(attrs) - 1):  # Exclude target
        gain = info_gain(rows, i)
        if gain > best_gain:
            best_gain = gain
            best_col = i
    
    # Build tree
    tree = {attrs[best_col]: {}}
    
    # Split by best attribute
    splits = {}
    for row in rows:
        val = row[best_col]
        if val not in splits:
            splits[val] = []
        splits[val].append(row)
    
    # Recursively build subtrees
    for val, subset in splits.items():
        # Remove used attribute
        new_rows = [[row[i] for i in range(len(row)) if i != best_col] for row in subset]
        new_attrs = [attrs[i] for i in range(len(attrs)) if i != best_col]
        tree[attrs[best_col]][val] = build_tree(new_rows, new_attrs)
    
    return tree

# Print tree
def print_tree(tree, indent=''):
    if not isinstance(tree, dict):
        print(f" -> {tree}")
        return
    for attr, branches in tree.items():
        for val, subtree in branches.items():
            print(f"\n{indent}{attr} = {val}", end='')
            print_tree(subtree, indent + '  ')

# Main
print("DECISION TREE - Play Outside")
print("="*40)
print("\nDataset:", attributes)
for i, row in enumerate(data, 1):
    print(f"{i}. {row}")

print("\n" + "="*40)
tree = build_tree(data, attributes)
print("\nDecision Tree:")
print_tree(tree)
print("\n" + "="*40)