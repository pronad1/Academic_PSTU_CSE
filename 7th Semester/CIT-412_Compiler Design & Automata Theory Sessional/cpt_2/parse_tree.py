
def build_tree(expression):
    expression = expression.replace(" ", "")

    # Find + or - operator
    for i in range(len(expression) - 1, -1, -1):
        if expression[i] in "+-":
            return {
                "list": [
                    build_tree(expression[:i]),
                    expression[i],
                    {"term": expression[i + 1:]}
                ]
            }

    # list -> term
    return {"list": {"term": expression}}


def print_tree(tree, prefix="", is_last=True):
    if isinstance(tree, dict):
        for key, value in tree.items():
            print(prefix + ("└── " if is_last else "├── ") + key)

            if isinstance(value, list):
                for i, item in enumerate(value):
                    print_tree(
                        item,
                        prefix + ("    " if is_last else "│   "),
                        i == len(value) - 1
                    )
            else:
                print_tree(value, prefix + ("    " if is_last else "│   "), True)

    else:
        print(prefix + ("└── " if is_last else "├── ") + str(tree))


# Main
expression = input("Enter Expression: ")

tree = build_tree(expression)

print("\nParse Tree:\n")
print_tree(tree)
