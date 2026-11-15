"""
Section 3.1 – The Role of the Lexical Analyzer
Tokenizer: breaks source code into (lexeme, token-type) pairs.

Token types used:
  KEYWORD          – reserved word of a programming language
  IDENTIFIER       – variable / function name
  NUMBER           – integer literal
  OPERATOR         – arithmetic / logical operator
  RELATIONAL_OP    – comparison operator
  SHIFT_OP         – bit-shift operator
  PUNCTUATION      – delimiters and separators  ({ } ; , etc.)
  HTML_TAG         – a complete angle-bracket tag  (<div>, </body> …)
  ERROR            – unrecognised single character
"""

# -----------------------------------------------------------------
# Keyword sets (kept as frozensets for O(1) lookup)
# -----------------------------------------------------------------
KEYWORDS = frozenset([
    # Python
    "False", "None", "True", "and", "as", "assert", "async", "await",
    "break", "class", "continue", "def", "del", "elif", "else", "except",
    "finally", "for", "from", "global", "if", "import", "in", "is",
    "lambda", "nonlocal", "not", "or", "pass", "raise", "return", "try",
    "while", "with", "yield",

    # C / C++ / Java / C#
    "auto", "bool", "byte", "case", "catch", "char", "checked", "const",
    "decimal", "default", "delegate", "do", "double", "dynamic", "enum",
    "event", "explicit", "extern", "finally", "fixed", "float",
    "foreach", "goto", "implicit", "int", "interface", "internal", "lock",
    "long", "namespace", "new", "null", "object", "operator", "out",
    "override", "params", "private", "protected", "public", "readonly",
    "ref", "sbyte", "sealed", "short", "sizeof", "stackalloc", "static",
    "string", "struct", "switch", "this", "throw", "typeof", "uint",
    "ulong", "unchecked", "unsafe", "ushort", "using", "virtual", "void",
    "volatile",

    # Other common languages
    "strictfp", "native", "transient", "synchronized", "abstract", "final",
    "extends", "implements", "instanceof", "package", "super",
    "throws", "var", "let",
])

OPERATORS       = frozenset(["+", "-", "*", "/", "=", "&", "|", "&&", "||"])
RELATIONAL_OPS  = frozenset(["==", "!=", "<", ">", "<=", ">="])
SHIFT_OPS       = frozenset(["<<", ">>"])
PUNCTUATION     = frozenset(["{", "}", "(", ")", "[", "]", ",", ";", ":"])


def simple_tokenizer(code):
    """
    Very simple whitespace-based tokenizer (no regex).
    Handles: keywords, identifiers, numbers, operators, punctuation, HTML tags.
    Demonstrates the concept of tokens/lexemes from Dragon Book §3.1.
    """
    raw_tokens = code.split()
    results = []

    for lexeme in raw_tokens:
        # --- trailing semicolon: split the identifier from ';' ---
        if lexeme.endswith(";") and lexeme != ";":
            core = lexeme[:-1]
            results.append((core,  _classify(core)))
            results.append((";",   "PUNCTUATION"))
            continue

        results.append((lexeme, _classify(lexeme)))

    return results


def _classify(lexeme):
    """Return the token type for a single lexeme."""
    if lexeme in KEYWORDS:
        return "KEYWORD"
    if lexeme in PUNCTUATION:
        return "PUNCTUATION"
    if lexeme in OPERATORS:
        return "OPERATOR"
    if lexeme in RELATIONAL_OPS:
        return "RELATIONAL_OP"
    if lexeme in SHIFT_OPS:
        return "SHIFT_OP"
    if lexeme.startswith("<") and lexeme.endswith(">"):
        return "HTML_TAG"
    if lexeme.lstrip("-").isdigit():          # integer (allow leading minus)
        return "NUMBER"
    if lexeme.replace(".", "", 1).lstrip("-").isdigit():
        return "NUMBER"                        # float
    if lexeme.isidentifier():
        return "IDENTIFIER"
    return "ERROR"


if __name__ == "__main__":
    sample_code = """if x >= y {
        int count = 10
        <div> hello </body>
    }"""
    print(f"Code:{sample_code}")
    print("\nTokens:")
    for lexeme, t_type in simple_tokenizer(sample_code):
        print(f"  <{t_type}, '{lexeme}'>")









# import re

# def library_tokenizer(code):
#     token_spec = [
#         ('HTML_TAG',   r'</?[a-zA-Z][a-zA-Z0-9]*>'),
#         ('KEYWORD',    r'\b(if|else|while|for|return|int|float|void|char)\b'),
#         ('RELOP',      r'==|!=|<=|>=|<|>'),
#         ('ASSIGN',     r'='),
#         ('ARITH_OP',   r'[+\-*/%]'),
#         ('NUMBER',     r'\b\d+(\.\d+)?\b'),
#         ('IDENTIFIER', r'\b[a-zA-Z_][a-zA-Z0-9_]*\b'),
#         ('PUNCTUATION',r'[{}();,]'),
#         ('SKIP',       r'[ \t\r\n]+'),       # Skip whitespace
#         ('MISMATCH',   r'.')                 # Any other character
#     ]

#     # Combine into a single regex with named groups
#     tok_regex = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_spec)
    
#     tokens = []
#     for mo in re.finditer(tok_regex, code):
#         kind = mo.lastgroup
#         value = mo.group()
#         if kind == 'SKIP':
#             continue
#         elif kind == 'MISMATCH':
#             tokens.append(('ERROR', value))
#         else:
#             tokens.append((kind, value))
#     return tokens


# if __name__ == "__main__":
#     sample_code = """if x >= y {
#         int count = 10
#         <div> hello </body>
#     }"""

#     for t_type, lexeme in library_tokenizer(sample_code):
#         print(f"  <{t_type}, '{lexeme}'>")