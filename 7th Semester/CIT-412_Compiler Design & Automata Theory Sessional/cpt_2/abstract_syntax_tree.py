
def build_tree(expression):
    expression = expression.replace(" ", "")

    # Remove outer parentheses
    while expression.startswith("(") and expression.endswith(")"):
        count = 0
        valid = True

        for i, ch in enumerate(expression):
            if ch == '(':
                count += 1
            elif ch == ')':
                count -= 1

            if count == 0 and i != len(expression) - 1:
                valid = False
                break

        if valid:
            expression = expression[1:-1]
        else:
            break

    # Operator precedence
    for operators in ["+-", "*/"]:
        count = 0

        for i in range(len(expression) - 1, -1, -1):
            ch = expression[i]

            if ch == ')':
                count += 1
            elif ch == '(':
                count -= 1

            elif count == 0 and ch in operators:
                if i == 0 or expression[i - 1] in "+-*/(":
                    continue

                return [
                    ch,
                    build_tree(expression[:i]),
                    build_tree(expression[i + 1:])
                ]

    return expression


def print_tree(tree, prefix="", is_left=True):
    if not isinstance(tree, list):
        print(prefix + ("└── " if is_left else "┌── ") + str(tree))
        return

    print_tree(
        tree[2],
        prefix + ("│   " if is_left else "    "),
        False
    )

    print(prefix + ("└── " if is_left else "┌── ") + tree[0])

    print_tree(
        tree[1],
        prefix + ("    " if is_left else "│   "),
        True
    )


# Main
expression = input("Enter Expression: ")

tree = build_tree(expression)

print("\nAbstract Syntax Tree:\n")
print_tree(tree)
