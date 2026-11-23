"""
==============================================================================
  CIT 412: Compiler Design and Automata Theory Sessional
  Chapter 02 | Section 2.3 — Syntax-Directed Translation (SDT)
  7th Semester (Level-4, Semester-I) | Session: 2021-22 / Jan-June 2025
  Reference: Dragon Book (Compilers: Principles, Techniques & Tools, 2nd Ed.)
==============================================================================

  PROBLEMS IN THIS FILE:
  ----------------------
  Problem 2.3.1 — Notation Conversion via SDT
                  (a) Infix → Prefix
                  (b) Postfix → Infix
                  (c) Postfix → Prefix
  Problem 2.3.2 — Value Translation: Integer ↔ Roman Numeral (SDT)
  Problem 2.3.3 — Annotated Parse Trees with Attribute Values

  Run this file:  python3 section_2_3_syntax_directed_translation.py
==============================================================================
"""

# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.3.1 — Notation Conversion via SDT                   ║
# ║  (a) Infix→Prefix  (b) Postfix→Infix  (c) Postfix→Prefix       ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Write syntax-directed translation schemes (SDTs) to convert:
#   (a) Infix arithmetic expressions into PREFIX (Polish) notation.
#   (b) Postfix arithmetic expressions into INFIX notation.
#   (c) Postfix arithmetic expressions directly into PREFIX notation.
#
# CONCEPT:
#   An SDT attaches SEMANTIC ACTIONS to grammar productions.
#   The actions run when the production is applied and build output.
#
#   (a) Infix→Prefix: use recursive descent; build "op left right" strings.
#       Grammar with SDT:
#         E → E + T  { E.code = "+ " + E1.code + " " + T.code }
#           | T
#         T → T * F  { T.code = "* " + T1.code + " " + F.code }
#           | F
#         F → ( E )  { F.code = E.code }
#           | id     { F.code = id }
#
#   (b) Postfix→Infix: stack-based.
#       Action on operator op: pop b,a → push "( a op b )"
#
#   (c) Postfix→Prefix: stack-based.
#       Action on operator op: pop b,a → push "op a b"
#
# INPUT (embedded):
INFIX_INPUTS   = ["3 + 4", "3 + 4 * 2", "( 3 + 4 ) * 2",
                  "10 - 2 * 3 + 1", "( a + b ) * ( c - d )"]
POSTFIX_INPUTS = ["3 4 +", "3 4 2 * +", "3 4 + 2 *",
                  "10 2 3 * - 1 +", "a b + c d - *"]


# ── Infix → Prefix (recursive descent SDT) ──────────────────────────

def infix_to_prefix(expr):
    """SDT: infix expression → prefix (Polish) string."""
    tz = expr.split()
    pos = [0]   # mutable index

    def parse_E():
        node = parse_T()
        while pos[0] < len(tz) and tz[pos[0]] in ('+', '-'):
            op = tz[pos[0]]; pos[0] += 1
            right = parse_T()
            node = f"{op} {node} {right}"   # semantic action
        return node

    def parse_T():
        node = parse_F()
        while pos[0] < len(tz) and tz[pos[0]] in ('*', '/'):
            op = tz[pos[0]]; pos[0] += 1
            right = parse_F()
            node = f"{op} {node} {right}"   # semantic action
        return node

    def parse_F():
        if tz[pos[0]] == '(':
            pos[0] += 1
            v = parse_E()
            pos[0] += 1   # ')'
            return v
        t = tz[pos[0]]; pos[0] += 1
        return t   # semantic action: emit operand

    return parse_E()


# ── Postfix → Infix (stack-based SDT) ───────────────────────────────

def postfix_to_infix(expr):
    """SDT: postfix expression → infix string (fully parenthesised)."""
    stack = []
    for tok in expr.split():
        if tok in ('+', '-', '*', '/'):
            b, a = stack.pop(), stack.pop()
            stack.append(f"( {a} {tok} {b} )")   # semantic action
        else:
            stack.append(tok)
    return stack[0]


# ── Postfix → Prefix (stack-based SDT) ──────────────────────────────

def postfix_to_prefix(expr):
    """SDT: postfix expression → prefix (Polish) string."""
    stack = []
    for tok in expr.split():
        if tok in ('+', '-', '*', '/'):
            b, a = stack.pop(), stack.pop()
            stack.append(f"{tok} {a} {b}")   # semantic action
        else:
            stack.append(tok)
    return stack[0]


def problem_2_3_1():
    print("=" * 70)
    print("  PROBLEM 2.3.1 — Notation Conversion via SDT")
    print("=" * 70)

    # (a) Infix → Prefix
    print("\n  (a) INFIX → PREFIX  (Recursive-Descent SDT)")
    print("      Grammar action: E+T → '+ ' + E.code + ' ' + T.code")
    print(f"\n  {'Infix Expression':<30} {'Prefix (Polish) Notation'}")
    print(f"  {'-'*30} {'-'*35}")
    for expr in INFIX_INPUTS:
        print(f"  {expr:<30} {infix_to_prefix(expr)}")

    # (b) Postfix → Infix
    print("\n  (b) POSTFIX → INFIX  (Stack-based SDT)")
    print("      Grammar action: E E op → push '( E1 op E2 )'")
    print(f"\n  {'Postfix Expression':<25} {'Infix Notation'}")
    print(f"  {'-'*25} {'-'*40}")
    for expr in POSTFIX_INPUTS:
        print(f"  {expr:<25} {postfix_to_infix(expr)}")

    # (c) Postfix → Prefix
    print("\n  (c) POSTFIX → PREFIX  (Stack-based SDT)")
    print("      Grammar action: E E op → push 'op E1 E2'")
    print(f"\n  {'Postfix Expression':<25} {'Prefix Notation'}")
    print(f"  {'-'*25} {'-'*35}")
    for expr in POSTFIX_INPUTS:
        print(f"  {expr:<25} {postfix_to_prefix(expr)}")
    print()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.3.2 — Value Translation: Integer ↔ Roman (SDT)      ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Create complete translation schemes to map:
#   (a) Integers (1–3999) → Roman numeral strings
#   (b) Roman numeral strings → Integers
#
# CONCEPT:
#   SYNTHESIZED ATTRIBUTES in the SDT:
#   - integer.roman is synthesized bottom-up from sub-parts:
#       integer.roman = thousands.roman + hundreds.roman +
#                       tens.roman + ones.roman
#   - Each sub-rule synthesizes its fragment independently.
#
#   Grammar (abbreviated):
#     integer   → thousands hundreds tens ones
#     thousands → M M M | M M | M | ε     { synthesize "MMM" etc. }
#     hundreds  → CM | CD | D? C* | ε     { synthesize "CM","CD" etc. }
#     tens      → XC | XL | L? X* | ε
#     ones      → IX | IV | V? I* | ε
#
# INPUT (embedded):
ROMAN_SDT_TESTS = [1, 4, 9, 14, 40, 90, 400, 900, 1000,
                   1994, 2024, 3549, 3999]

_MAP = [(1000,"M"),(900,"CM"),(500,"D"),(400,"CD"),(100,"C"),
        (90,"XC"),(50,"L"),(40,"XL"),(10,"X"),(9,"IX"),
        (5,"V"),(4,"IV"),(1,"I")]

def int_to_roman_sdt(n):
    """SDT synthesized attribute: integer → Roman numeral string."""
    if not (1 <= n <= 3999): return "OUT OF RANGE"
    r = ""
    for val, sym in _MAP:
        while n >= val: r += sym; n -= val   # semantic action
    return r

def roman_to_int_sdt(s):
    """SDT synthesized attribute: Roman numeral string → integer."""
    vals = {'I':1,'V':5,'X':10,'L':50,'C':100,'D':500,'M':1000}
    total, prev = 0, 0
    for ch in reversed(s):
        v = vals.get(ch, 0)
        total += v if v >= prev else -v   # semantic action
        prev = v
    return total

def show_annotated_tree(n):
    """Show annotated parse tree for integer → Roman SDT."""
    roman = int_to_roman_sdt(n)
    print(f"\n  Annotated Parse Tree for  {n}  →  '{roman}':")
    print(f"  integer (val = {n})")
    rem = n
    for grp, pairs in [
        ("thousands", [(1000,"M")]),
        ("hundreds",  [(900,"CM"),(500,"D"),(400,"CD"),(100,"C")]),
        ("tens",      [(90,"XC"),(50,"L"),(40,"XL"),(10,"X")]),
        ("ones",      [(9,"IX"),(5,"V"),(4,"IV"),(1,"I")]),
    ]:
        frag = ""
        for val, sym in pairs:
            while rem >= val: frag += sym; rem -= val
        print(f"    ├── {grp:<12} .roman = \"{frag if frag else 'ε'}\"")

def problem_2_3_2():
    print("=" * 70)
    print("  PROBLEM 2.3.2 — Value Translation: Integer ↔ Roman Numeral (SDT)")
    print("=" * 70)

    print("\n  Grammar (synthesized attribute .roman):")
    print("    integer   → thousands hundreds tens ones")
    print("    thousands → M M M | M M | M | ε     { .roman = 'M...' }")
    print("    hundreds  → CM | CD | D... | ε       { .roman = 'CM'... }")
    print("    tens      → XC | XL | L... | ε       { .roman = 'XC'... }")
    print("    ones      → IX | IV | V... | ε       { .roman = 'IX'... }")

    # (a) Integer → Roman
    print("\n  (a) Integer → Roman Numeral:")
    print(f"  {'Integer':<10} {'Roman':<20} {'Back-verified':<15} {'OK?'}")
    print(f"  {'-'*10} {'-'*20} {'-'*15} {'-'*5}")
    for n in ROMAN_SDT_TESTS:
        roman = int_to_roman_sdt(n)
        back  = roman_to_int_sdt(roman)
        print(f"  {n:<10} {roman:<20} {back:<15} {'YES' if back==n else 'NO'}")

    # (b) Roman → Integer
    print("\n  (b) Roman Numeral → Integer:")
    roman_strings = [int_to_roman_sdt(n) for n in ROMAN_SDT_TESTS]
    print(f"  {'Roman String':<20} {'Integer'}")
    print(f"  {'-'*20} {'-'*10}")
    for s in roman_strings:
        print(f"  {s:<20} {roman_to_int_sdt(s)}")

    # Annotated trees
    print("\n  (c) Annotated Parse Trees:")
    for n in [1994, 2024]:
        show_annotated_tree(n)
    print()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.3.3 — Annotated Parse Trees with Attribute Values   ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Draw annotated parse trees for the following infix expressions,
#   showing explicit .val attribute at EVERY node of the tree:
#   (a) 3 + 4
#   (b) 3 + 4 * 2
#   (c) ( 3 + 4 ) * 2
#
# CONCEPT:
#   - Each node carries a synthesized attribute .val.
#   - Attributes are computed BOTTOM-UP (leaves first, root last).
#   - Grammar with SDT:
#       E → E + T  { E.val = E1.val + T.val }
#       E → T       { E.val = T.val }
#       T → T * F  { T.val = T1.val * F.val }
#       T → F       { T.val = F.val }
#       F → ( E )   { F.val = E.val }
#       F → num     { F.val = num }
#
# INPUT (embedded):
ANNOTATED_INPUTS = ["3 + 4", "3 + 4 * 2", "( 3 + 4 ) * 2"]


class ASTNode:
    def __init__(self, label, val=None, children=None):
        self.label    = label
        self.val      = val
        self.children = children or []


class AnnotatedParser:
    """Builds annotated AST while parsing (SDT with synthesized attributes)."""
    def __init__(self, text):
        self.tokens = text.split()
        self.pos = 0

    def peek(self): return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def consume(self): t = self.tokens[self.pos]; self.pos += 1; return t

    def parse_E(self):
        node = self.parse_T()
        while self.peek() in ('+', '-'):
            op    = self.consume()
            right = self.parse_T()
            new_v = node.val + right.val if op == '+' else node.val - right.val
            node  = ASTNode(f"E (={new_v})", new_v,
                            [node, ASTNode(op), right])
        return node

    def parse_T(self):
        node = self.parse_F()
        while self.peek() in ('*', '/'):
            op    = self.consume()
            right = self.parse_F()
            new_v = node.val * right.val if op == '*' else node.val // right.val
            node  = ASTNode(f"T (={new_v})", new_v,
                            [node, ASTNode(op), right])
        return node

    def parse_F(self):
        if self.peek() == '(':
            self.consume()
            inner = self.parse_E()
            self.consume()
            node  = ASTNode(f"F (={inner.val})", inner.val,
                            [ASTNode('('), inner, ASTNode(')')])
            return node
        val = int(self.consume())
        return ASTNode(f"F (={val})", val, [ASTNode(str(val), val)])


def print_tree(node, prefix="", is_last=True):
    connector   = "└── " if is_last else "├── "
    child_pfx   = prefix + ("    " if is_last else "│   ")
    print(prefix + connector + node.label)
    for i, child in enumerate(node.children):
        print_tree(child, child_pfx, i == len(node.children) - 1)


def collect_steps(node, steps):
    for c in node.children: collect_steps(c, steps)
    if node.val is not None: steps.append((node.label, node.val))


def problem_2_3_3():
    print("=" * 70)
    print("  PROBLEM 2.3.3 — Annotated Parse Trees with Attribute Values")
    print("=" * 70)
    print("""
  Grammar with Synthesized Attributes:
    E → E + T  { E.val = E1.val + T.val }
    E → T       { E.val = T.val }
    T → T * F  { T.val = T1.val * F.val }
    T → F       { T.val = F.val }
    F → ( E )   { F.val = E.val }
    F → num     { F.val = num }
""")
    for expr in ANNOTATED_INPUTS:
        print(f"  Input: \"{expr}\"")
        print("  " + "-" * 50)
        parser = AnnotatedParser(expr)
        root   = parser.parse_E()
        print(f"  Root .val = {root.val}\n")
        print_tree(root, "  ")
        print()
        steps = []
        collect_steps(root, steps)
        print("  Bottom-up .val computation:")
        print(f"  {'Node':<25} {'Synthesized .val'}")
        print(f"  {'-'*25} {'-'*16}")
        for label, val in steps:
            print(f"  {label:<25} {val}")
        print()


# ══════════════════════════════════════════════════════════════════════
#  MAIN — Run all problems in order
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    problem_2_3_1()
    problem_2_3_2()
    problem_2_3_3()
