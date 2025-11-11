"""
DECISION TREE - Simple Implementation for Final Exam
Dataset: Buy Computer (Age, Income, Student, Credit -> Buy)
Algorithm: ID3 using Information Gain
"""

import math

# Dataset: Will customer buy a computer?
data = [
    ['Young', 'High', 'No', 'Fair', 'No'],
    ['Young', 'High', 'No', 'Good', 'No'],
    ['Middle', 'High', 'No', 'Fair', 'Yes'],
    ['Senior', 'Medium', 'No', 'Fair', 'Yes'],
    ['Senior', 'Low', 'Yes', 'Fair', 'Yes'],
    ['Senior', 'Low', 'Yes', 'Good', 'No'],
    ['Middle', 'Low', 'Yes', 'Good', 'Yes'],
    ['Young', 'Medium', 'No', 'Fair', 'No'],
    ['Young', 'Low', 'Yes', 'Fair', 'Yes'],
    ['Senior', 'Medium', 'Yes', 'Fair', 'Yes']
]

attributes = ['Age', 'Income', 'Student', 'Credit', 'Buy']

# Calculate entropy
def entropy(data, target_idx):
    counts = {}
    for row in data:
        label = row[target_idx]
        counts[label] = counts.get(label, 0) + 1
    
    ent = 0
    total = len(data)
    for count in counts.values():
        p = count / total
        ent -= p * math.log2(p)
    return ent

# Calculate information gain
def info_gain(data, attr_idx, target_idx):
    total_ent = entropy(data, target_idx)
    
    # Split by attribute
    splits = {}
    for row in data:
        val = row[attr_idx]
        if val not in splits:
            splits[val] = []
        splits[val].append(row)
    
    # Weighted entropy
    weighted_ent = 0
    for subset in splits.values():
        weighted_ent += (len(subset) / len(data)) * entropy(subset, target_idx)
    
    return total_ent - weighted_ent

# Build decision tree
def build_tree(data, attrs, target='Buy'):
    target_idx = attrs.index(target)
    labels = [row[target_idx] for row in data]
    
    # All same label
    if len(set(labels)) == 1:
        return labels[0]
    
    # No more attributes
    if len(attrs) == 1:
        return max(set(labels), key=labels.count)
    
    # Find best attribute
    best_attr = None
    best_gain = -1
    for i, attr in enumerate(attrs):
        if attr != target:
            gain = info_gain(data, i, target_idx)
            if gain > best_gain:
                best_gain = gain
                best_attr = attr
    
    # Create tree
    tree = {best_attr: {}}
    best_idx = attrs.index(best_attr)
    
    # Build subtrees
    values = set(row[best_idx] for row in data)
    for val in values:
        subset = [row for row in data if row[best_idx] == val]
        new_attrs = [a for a in attrs if a != best_attr]
        tree[best_attr][val] = build_tree(subset, new_attrs, target)
    
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
if __name__ == "__main__":
    print("="*50)
    print("DECISION TREE - Buy Computer Dataset")
    print("="*50)
    
    print("\nDataset:")
    print(attributes)
    for i, row in enumerate(data, 1):
        print(f"{i:2}. {row}")
    
    print("\n" + "="*50)
    tree = build_tree(data, attributes)
    
    print("\nDecision Tree:")
    print_tree(tree)
    
    print("\n" + "="*50)
