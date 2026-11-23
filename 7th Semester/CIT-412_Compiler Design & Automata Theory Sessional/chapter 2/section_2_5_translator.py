"""
==============================================================================
  CIT 412: Compiler Design and Automata Theory Sessional
  Chapter 02 | Section 2.5 — A Translator for Simple Expressions
  7th Semester (Level-4, Semester-I) | Session: 2021-22 / Jan-June 2025
  Reference: Dragon Book (Compilers: Principles, Techniques & Tools, 2nd Ed.)
==============================================================================

  PROBLEMS IN THIS FILE:
  ----------------------
  Problem 2.5.1 — Build a Complete Infix-to-Postfix Translator (Mini-Compiler)
                  Structure: Lexer → Parser (expr/term/factor) + SDT → Output

  Run this file:  python3 section_2_5_translator.py
==============================================================================
"""

# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.5.1 — Complete Infix-to-Postfix Mini-Compiler        ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Structure the parser classes/functions (expr, term, factor) into a
#   UNIFIED, EXECUTABLE translator module that converts infix arithmetic
#   expressions into postfix output using syntax-directed translation.
#   This is the complete translator described in Section 2.5 of Dragon Book.
#
# CONCEPT:
#   PIPELINE:
#     Source Text → [LEXER] → Token Stream → [PARSER + SDT] → Postfix Output
#
#   GRAMMAR with embedded SDT semantic actions { ... }:
#     expr      → term  rest_expr
#     rest_expr → + term { emit('+') } rest_expr
#               | - term { emit('-') } rest_expr
#               | ε
#     term      → factor  rest_term
#     rest_term → * factor { emit('*') } rest_term
#               | / factor { emit('/') } rest_term
#               | ε
#     factor    → ( expr )
#               | num  { emit(num) }
#               | id   { emit(id) }
#
#   KEY IDEA: emit() fires AFTER the operand(s) are processed,
#   placing the operator in POSTFIX position.
#
# INPUT (embedded):
TRANSLATOR_TESTS = [
    "9 - 5 + 2",
    "9 - 5 * 2",
    "( 9 - 5 ) * 2",
    "a + b * c",
    "( a + b ) * ( c - d )",
    "x * y + z / 2",
    "1 + 2 + 3 + 4",
    "( 1 + 2 ) * ( 3 + 4 ) - 5",
]


# ══════════════════════════════════════════════════════════════════════
#  COMPONENT 1 — LEXER
#  Converts raw text into a stream of Token objects
# ══════════════════════════════════════════════════════════════════════

class Token:
    NUM    = "NUM"
    ID     = "ID"
    PLUS   = "+"
    SUB    = "-"
    MUL    = "*"
    DIV    = "/"
    LPAREN = "("
    RPAREN = ")"
    EOF    = "EOF"

    def __init__(self, kind, value=None):
        self.kind  = kind
        self.value = value

    def __repr__(self):
        return f"Token({self.kind}, {self.value!r})"


class Lexer:
    """
    Tokeniser for arithmetic expressions.
    Supports: integers, identifiers (a-z), +, -, *, /, (, )
    """
    _OPERATORS = {
        '+': Token.PLUS, '-': Token.SUB,
        '*': Token.MUL,  '/': Token.DIV,
        '(': Token.LPAREN, ')': Token.RPAREN,
    }

    def __init__(self, text):
        self.text = text
        self.pos  = 0

    def _skip_ws(self):
        while self.pos < len(self.text) and self.text[self.pos].isspace():
            self.pos += 1

    def next_token(self):
        self._skip_ws()
        if self.pos >= len(self.text):
            return Token(Token.EOF)
        ch = self.text[self.pos]

        # Number
        if ch.isdigit():
            start = self.pos
            while self.pos < len(self.text) and self.text[self.pos].isdigit():
                self.pos += 1
            return Token(Token.NUM, int(self.text[start:self.pos]))

        # Identifier
        if ch.isalpha() or ch == '_':
            start = self.pos
            while self.pos < len(self.text) and (self.text[self.pos].isalnum() or self.text[self.pos] == '_'):
                self.pos += 1
            return Token(Token.ID, self.text[start:self.pos])

        # Operator / bracket
        if ch in self._OPERATORS:
            self.pos += 1
            return Token(self._OPERATORS[ch], ch)

        raise ValueError(f"Unknown character: {ch!r}")


# ══════════════════════════════════════════════════════════════════════
#  COMPONENT 2 — PARSER + SDT (infix → postfix)
#  Recursive-descent parser with inline emit() semantic actions
# ══════════════════════════════════════════════════════════════════════

class InfixToPostfixTranslator:
    """
    The TRANSLATOR: combines parser (expr/term/factor) with SDT.

    Parser functions:
      _parse_expr()       → E  → term rest_expr
      _parse_rest_expr()  → E' → + term {emit} rest_expr | - term {emit} rest_expr | ε
      _parse_term()       → T  → factor rest_term
      _parse_rest_term()  → T' → * factor {emit} rest_term | / factor {emit} rest_term | ε
      _parse_factor()     → F  → ( expr ) | num {emit} | id {emit}
    """

    def __init__(self, text):
        self.lexer   = Lexer(text)
        self.current = self.lexer.next_token()   # one-token lookahead
        self.output  = []                        # postfix token accumulator

    def _emit(self, tok_str):
        """Semantic action: add token to postfix output."""
        self.output.append(tok_str)

    def _match(self, kind):
        """Consume lookahead if it matches 'kind'; otherwise SyntaxError."""
        if self.current.kind != kind:
            raise SyntaxError(f"Expected '{kind}', got '{self.current.kind}'")
        self.current = self.lexer.next_token()

    def translate(self):
        """Entry point: translate and return the postfix string."""
        self._parse_expr()
        return " ".join(str(t) for t in self.output)

    # ── expr: E → T E' ──────────────────────────────────────────────
    def _parse_expr(self):
        self._parse_term()
        self._parse_rest_expr()

    # ── rest_expr: E' → + T {emit('+')} E' | - T {emit('-')} E' | ε ─
    def _parse_rest_expr(self):
        if self.current.kind == Token.PLUS:
            self._match(Token.PLUS)
            self._parse_term()
            self._emit('+')            # ← semantic action fires AFTER term
            self._parse_rest_expr()
        elif self.current.kind == Token.SUB:
            self._match(Token.SUB)
            self._parse_term()
            self._emit('-')            # ← semantic action
            self._parse_rest_expr()
        # else ε: do nothing

    # ── term: T → F T' ──────────────────────────────────────────────
    def _parse_term(self):
        self._parse_factor()
        self._parse_rest_term()

    # ── rest_term: T' → * F {emit('*')} T' | / F {emit('/')} T' | ε ─
    def _parse_rest_term(self):
        if self.current.kind == Token.MUL:
            self._match(Token.MUL)
            self._parse_factor()
            self._emit('*')            # ← semantic action
            self._parse_rest_term()
        elif self.current.kind == Token.DIV:
            self._match(Token.DIV)
            self._parse_factor()
            self._emit('/')            # ← semantic action
            self._parse_rest_term()

    # ── factor: F → ( expr ) | num {emit(num)} | id {emit(id)} ──────
    def _parse_factor(self):
        if self.current.kind == Token.LPAREN:
            self._match(Token.LPAREN)
            self._parse_expr()
            self._match(Token.RPAREN)
        elif self.current.kind == Token.NUM:
            self._emit(str(self.current.value))   # ← semantic action
            self._match(Token.NUM)
        elif self.current.kind == Token.ID:
            self._emit(self.current.value)        # ← semantic action
            self._match(Token.ID)
        else:
            raise SyntaxError(f"Unexpected token in factor: '{self.current.kind}'")


# ══════════════════════════════════════════════════════════════════════
#  PROBLEM 2.5.1 — Display and Run
# ══════════════════════════════════════════════════════════════════════

def problem_2_5_1():
    print("=" * 70)
    print("  PROBLEM 2.5.1 — Complete Infix-to-Postfix Translator (Mini-Compiler)")
    print("=" * 70)
    print("""
  TRANSLATOR PIPELINE:
    Source Text → Lexer → Token Stream → Parser + SDT → Postfix Output

  GRAMMAR with Semantic Actions { emit(...) }:
    expr      → term  rest_expr
    rest_expr → + term { emit('+') } rest_expr
              | - term { emit('-') } rest_expr
              | ε
    term      → factor  rest_term
    rest_term → * factor { emit('*') } rest_term
              | / factor { emit('/') } rest_term
              | ε
    factor    → ( expr )
              | num  { emit(num) }
              | id   { emit(id) }

  KEY: emit() fires AFTER operands → operator appears in postfix position.

  LEXER tokens: NUM, ID, +, -, *, /, (, ), EOF
""")

    print("  TRANSLATION RESULTS:")
    print(f"  {'Infix Expression':<35} {'Postfix Output'}")
    print(f"  {'-'*35} {'-'*35}")
    for expr in TRANSLATOR_TESTS:
        t      = InfixToPostfixTranslator(expr)
        result = t.translate()
        print(f"  {expr:<35} {result}")

    # Show how postfix output is built step-by-step for one example
    demo_expr = "( a + b ) * ( c - d )"
    print(f"\n  EMIT SEQUENCE for: \"{demo_expr}\"")
    print("  " + "-" * 55)

    class TracingTranslator(InfixToPostfixTranslator):
        def _emit(self, tok_str):
            print(f"    emit('{tok_str}')  → output so far: {self.output + [tok_str]}")
            super()._emit(tok_str)

    t = TracingTranslator(demo_expr)
    result = t.translate()
    print(f"\n  Final postfix: \"{result}\"")
    print()


if __name__ == "__main__":
    problem_2_5_1()
