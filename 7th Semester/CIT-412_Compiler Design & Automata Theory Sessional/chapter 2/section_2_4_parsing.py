"""
==============================================================================
  CIT 412: Compiler Design and Automata Theory Sessional
  Chapter 02 | Section 2.4 — Parsing (Top-Down / Recursive Descent)
  7th Semester (Level-4, Semester-I) | Session: 2021-22 / Jan-June 2025
  Reference: Dragon Book (Compilers: Principles, Techniques & Tools, 2nd Ed.)
==============================================================================

  PROBLEMS IN THIS FILE:
  ----------------------
  Problem 2.4.1 — Left-Recursion Elimination
  Problem 2.4.2 — Recursive-Descent Parser Implementation
                  (with full call trace and function stubs)

  Run this file:  python3 section_2_4_parsing.py
==============================================================================
"""

# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.4.1 — Left-Recursion Elimination                    ║
# ║  Transform grammar to be suitable for predictive parsing        ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   The grammar below has LEFT RECURSION, which makes top-down
#   parsing impossible (infinite loop).  Eliminate left recursion
#   to get an equivalent grammar suitable for recursive descent.
#
#   ORIGINAL (left-recursive):
#       E  →  E + T  |  E - T  |  T
#       T  →  T * F  |  T / F  |  F
#       F  →  ( E )  |  num
#
#   TRANSFORMED (right-recursive, no left recursion):
#       E   →  T  E'
#       E'  →  + T E'  |  - T E'  |  ε
#       T   →  F  T'
#       T'  →  * F T'  |  / F T'  |  ε
#       F   →  ( E )   |  num
#
# CONCEPT:
#   General left-recursion elimination formula:
#     A → A α | β   becomes:   A → β A'
#                               A' → α A' | ε
#   Applied:   E → E+T | T   gives:   E → T E',   E' → +T E' | ε

def problem_2_4_1():
    print("=" * 65)
    print("  PROBLEM 2.4.1 — Left-Recursion Elimination")
    print("=" * 65)
    print("""
  ORIGINAL grammar (left-recursive — causes infinite loop in top-down):
    E  →  E + T  |  E - T  |  T
    T  →  T * F  |  T / F  |  F
    F  →  ( E )  |  num

  WHY IT FAILS (top-down):
    To parse E, we apply E → E + T.
    But parsing the new E again applies E → E + T. → Infinite loop!

  ─────────────────────────────────────────────────────────────────
  Elimination formula:
    A → A α₁ | A α₂ | β     becomes:
        A  → β A'
        A' → α₁ A' | α₂ A' | ε

  Applied to E:
    A = E,  α₁ = "+T",  α₂ = "-T",  β = "T"
    E  → T E'
    E' → + T E'  |  - T E'  |  ε

  Applied to T:
    A = T,  α₁ = "*F",  α₂ = "/F",  β = "F"
    T  → F T'
    T' → * F T'  |  / F T'  |  ε

  ─────────────────────────────────────────────────────────────────
  TRANSFORMED grammar (RIGHT-recursive — suitable for recursive descent):
    E   →  T  E'
    E'  →  + T E'  |  - T E'  |  ε
    T   →  F  T'
    T'  →  * F T'  |  / F T'  |  ε
    F   →  ( E )   |  num

  Each non-terminal → one function in the recursive-descent parser.
""")


# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.4.2 — Recursive-Descent Parser Implementation        ║
# ║  Implement parser functions for the transformed grammar          ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Write recursive-descent (predictive) parser functions in Python
#   for the transformed grammar from Problem 2.4.1.
#   Each non-terminal is handled by one function.
#   Show: (a) test results for several expressions,
#         (b) full call trace for one expression.
#
# CONCEPT:
#   PREDICTIVE PARSING:
#   - Look at the NEXT token (lookahead) to decide which rule to apply.
#   - No backtracking needed if the grammar is LL(1).
#   - match(t): consume next token if it equals t, else raise SyntaxError.
#   - For E', look at lookahead:
#       if '+' or '-' → apply rule with operator
#       else          → apply ε (do nothing)
#
# INPUT (embedded):
PARSER_TESTS = [
    ("3 + 4",             7),
    ("10 - 3 * 2",        4),
    ("( 10 - 3 ) * 2",   14),
    ("6 / 2 + 1",         4),
    ("( 2 + 3 ) * ( 4 - 1 )", 15),
    ("100 / 5 / 2",      10),
    ("1 + 2 + 3 + 4",    10),
]


class TokenStream:
    """Manages the token stream for the parser."""
    EOF = "$"

    def __init__(self, text):
        self.tokens = text.split() + [self.EOF]
        self.pos    = 0
        self.log    = []   # call trace

    def lookahead(self):
        return self.tokens[self.pos]

    def match(self, expected):
        """Consume token if it matches; raise SyntaxError otherwise."""
        actual = self.tokens[self.pos]
        if actual != expected:
            raise SyntaxError(f"Expected '{expected}', got '{actual}'")
        self.log.append(f"  match('{expected}')")
        self.pos += 1

    def consume_num(self):
        tok = self.tokens[self.pos]
        self.log.append(f"  match(num='{tok}')")
        self.pos += 1
        return int(tok)


class RecursiveDescentParser:
    """
    Predictive recursive-descent parser.
    One method per non-terminal:
      parse_E()       → handles  E  → T E'
      parse_Eprime()  → handles  E' → + T E' | - T E' | ε
      parse_T()       → handles  T  → F T'
      parse_Tprime()  → handles  T' → * F T' | / F T' | ε
      parse_F()       → handles  F  → ( E ) | num
    """

    def __init__(self, text):
        self.ts = TokenStream(text)

    def parse(self):
        val = self.parse_E()
        self.ts.match("$")
        return val

    # ── Stub: E → T E' ──────────────────────────────────────────────
    def parse_E(self):
        self.ts.log.append("  call E()")
        t   = self.parse_T()
        val = self.parse_Eprime(t)
        self.ts.log.append(f"  return E() = {val}")
        return val

    # ── Stub: E' → + T E' | - T E' | ε ─────────────────────────────
    def parse_Eprime(self, inh):
        self.ts.log.append("  call E'()")
        la = self.ts.lookahead()
        if la == '+':
            self.ts.match('+')
            t = self.parse_T()
            return self.parse_Eprime(inh + t)
        elif la == '-':
            self.ts.match('-')
            t = self.parse_T()
            return self.parse_Eprime(inh - t)
        else:
            self.ts.log.append("  E' → ε")
            return inh   # ε production

    # ── Stub: T → F T' ──────────────────────────────────────────────
    def parse_T(self):
        self.ts.log.append("  call T()")
        f   = self.parse_F()
        val = self.parse_Tprime(f)
        self.ts.log.append(f"  return T() = {val}")
        return val

    # ── Stub: T' → * F T' | / F T' | ε ─────────────────────────────
    def parse_Tprime(self, inh):
        self.ts.log.append("  call T'()")
        la = self.ts.lookahead()
        if la == '*':
            self.ts.match('*')
            f = self.parse_F()
            return self.parse_Tprime(inh * f)
        elif la == '/':
            self.ts.match('/')
            f = self.parse_F()
            return self.parse_Tprime(inh // f)
        else:
            self.ts.log.append("  T' → ε")
            return inh

    # ── Stub: F → ( E ) | num ───────────────────────────────────────
    def parse_F(self):
        self.ts.log.append("  call F()")
        la = self.ts.lookahead()
        if la == '(':
            self.ts.match('(')
            val = self.parse_E()
            self.ts.match(')')
            self.ts.log.append(f"  return F() = {val}")
            return val
        else:
            val = self.ts.consume_num()
            self.ts.log.append(f"  return F() = {val}")
            return val


def problem_2_4_2():
    print("=" * 65)
    print("  PROBLEM 2.4.2 — Recursive-Descent Parser Implementation")
    print("=" * 65)
    print("""
  Transformed grammar (from Problem 2.4.1):
    E   →  T  E'
    E'  →  + T E'  |  - T E'  |  ε
    T   →  F  T'
    T'  →  * F T'  |  / F T'  |  ε
    F   →  ( E )   |  num

  LOOKAHEAD-based decision table:
    E'  : lookahead '+' → first alt | '-' → second alt | else → ε
    T'  : lookahead '*' → first alt | '/' → second alt | else → ε
    F   : lookahead '(' → parenthesised expr | else → number
""")

    # (a) Test results
    print("  (a) TEST RESULTS:")
    print(f"  {'Expression':<30} {'Expected':<12} {'Got':<10} {'OK?'}")
    print(f"  {'-'*30} {'-'*12} {'-'*10} {'-'*5}")
    for expr, expected in PARSER_TESTS:
        result = RecursiveDescentParser(expr).parse()
        ok     = "YES" if result == expected else "NO"
        print(f"  {expr:<30} {expected:<12} {result:<10} {ok}")

    # (b) Call trace
    trace_expr = "( 2 + 3 ) * ( 4 - 1 )"
    print(f"\n  (b) FULL CALL TRACE for: \"{trace_expr}\"")
    print("  " + "-" * 50)
    p = RecursiveDescentParser(trace_expr)
    r = p.parse()
    print(f"  Result = {r}\n")
    for line in p.ts.log:
        print(line)
    print()


# ══════════════════════════════════════════════════════════════════════
#  MAIN — Run all problems in order
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    problem_2_4_1()
    problem_2_4_2()
