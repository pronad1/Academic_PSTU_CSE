
def infix_to_postfix(expression):
    stack = []
    postfix = ""

    precedence = {
        '+': 1,
        '-': 1,
        '*': 2,
        '/': 2,
        '^': 3
    }

    for ch in expression:
        if ch == ' ':
            continue

        # Operand
        if ch.isalnum():
            postfix += ch

        # Opening parenthesis
        elif ch == '(':
            stack.append(ch)

        # Closing parenthesis
        elif ch == ')':
            while stack and stack[-1] != '(':
                postfix += stack.pop()

            if stack:
                stack.pop()

        # Operator
        else:
            while (stack and stack[-1] != '(' and
                   precedence.get(stack[-1], 0) >= precedence.get(ch, 0)):
                postfix += stack.pop()

            stack.append(ch)

    # Pop remaining operators
    while stack:
        postfix += stack.pop()

    return postfix


# Main
expression = input("Enter Infix Expression: ")

result = infix_to_postfix(expression)

print("Postfix Expression:", result)
