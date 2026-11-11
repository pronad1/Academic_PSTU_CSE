
def remove_whitespace_comments(code):

    result = []
    i = 0

    while i < len(code):

        # Remove single-line comments
        if code[i:i+2] == "//":
            while i < len(code) and code[i] != '\n':
                i += 1

        # Remove multi-line comments
        elif code[i:i+2] == "/*":
            i += 2

            while i < len(code) and code[i:i+2] != "*/":
                i += 1

            i += 2

        # Remove white spaces
        elif code[i].isspace():
            i += 1

        else:
            result.append(code[i])
            i += 1

    return ''.join(result)


code = """
int a = 10;  // variable

int b = 20;

/* This is
a comment */
"""

print("Original Code:")
print(code)

print("After Removing:")
print(remove_whitespace_comments(code))
