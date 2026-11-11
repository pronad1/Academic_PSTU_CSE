
# Manually created Keyword Symbol Table
symbol_table = [
    "if", "else", "elif", "while", "for",
    "break", "continue", "return", "def",
    "class", "int", "float", "char",
    "void", "import", "from", "as",
    "try", "except", "finally", "True",
    "False", "None", "and", "or", "not"
]

word = input("Enter a word: ")

if word in symbol_table:
    print(word, "is a Keyword")

elif word.isalpha() and not word[0].isdigit():
    print(word, "is an Identifier")

else:
    print(word, "is Invalid")
