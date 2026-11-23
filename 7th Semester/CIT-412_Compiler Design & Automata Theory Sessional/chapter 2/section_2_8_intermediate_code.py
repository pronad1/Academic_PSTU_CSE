"""
==============================================================================
  CIT 412: Compiler Design and Automata Theory Sessional
  Chapter 02 | Section 2.8 — Intermediate Code Generation
  7th Semester (Level-4, Semester-I) | Session: 2021-22 / Jan-June 2025
  Reference: Dragon Book (Compilers: Principles, Techniques & Tools, 2nd Ed.)
==============================================================================

  PROBLEMS IN THIS FILE:
  ----------------------
  Problem 2.8.1 — AST Construction: Node-creation functions for
                  expressions and assignment statements
  Problem 2.8.2 — Three-Address Code Generation from ASTs
                  (using temporaries t1, t2, t3, ...)
  Problem 2.8.3 — Control-Flow Code Generation
                  (while, if-else, boolean and/or/not)

  Run this file:  python3 section_2_8_intermediate_code.py
==============================================================================
"""

# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.8.1 — AST Construction                               ║
# ║  Node-creation functions for expressions & assignment stmts     ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Write node-creation functions to build abstract syntax trees (ASTs)
#   for expressions and assignment statements.  Display the resulting trees.
#
# CONCEPT:
#   ABSTRACT SYNTAX TREE (AST) vs CONCRETE PARSE TREE:
#     - Parse tree: includes every grammar symbol (including ε, brackets).
#     - AST: stripped of punctuation; only semantically meaningful nodes.
#
#   ABSTRACT SYNTAX GRAMMAR (for expressions):
#     assign  →  id '=' expr
#     expr    →  expr op expr  |  num  |  id
#     op      →  '+'  |  '-'  |  '*'  |  '/'
#
#   NODE-CREATION FUNCTIONS (Dragon Book style):
#     make_binop(op, left, right)  → binary operator node
#     make_assign(target, value)   → assignment node
#     make_var(name)               → variable (leaf)
#     make_num(value)              → numeric literal (leaf)
#
# INPUT (embedded):
AST_INPUTS = [
    "x = a + b * c",
    "y = ( a - b ) * ( c + d )",
    "z = a * b + c * d - e",
]


# ── AST Node types ───────────────────────────────────────────────────

class ASTNode:
    """Base class for all AST nodes."""
    pass

class BinOp(ASTNode):
    def __init__(self, op, left, right):
        self.op = op; self.left = left; self.right = right

class Assign(ASTNode):
    def __init__(self, target, value):
        self.target = target; self.value = value

class Num(ASTNode):
    def __init__(self, value):
        self.value = value

class Var(ASTNode):
    def __init__(self, name):
        self.name = name


# ── Node-creation functions (Dragon Book §2.8 style) ─────────────────

def make_binop(op, left, right): return BinOp(op, left, right)
def make_assign(target, value):  return Assign(target, value)
def make_num(v):                 return Num(v)
def make_var(n):                 return Var(n)


# ── AST Parser (builds tree instead of evaluating) ───────────────────

class ASTParser:
    def __init__(self, text):
        self.tokens = text.split(); self.pos = 0

    def peek(self):    return self.tokens[self.pos] if self.pos < len(self.tokens) else None
    def consume(self): t = self.tokens[self.pos]; self.pos += 1; return t

    def parse_assign(self):
        target = self.consume()   # variable name
        self.consume()            # '='
        value  = self.parse_expr()
        return make_assign(target, value)

    def parse_expr(self):
        node = self.parse_term()
        while self.peek() in ('+', '-'):
            op = self.consume(); right = self.parse_term()
            node = make_binop(op, node, right)
        return node

    def parse_term(self):
        node = self.parse_factor()
        while self.peek() in ('*', '/'):
            op = self.consume(); right = self.parse_factor()
            node = make_binop(op, node, right)
        return node

    def parse_factor(self):
        t = self.peek()
        if t == '(':
            self.consume(); v = self.parse_expr(); self.consume(); return v
        t = self.consume()
        try: return make_num(int(t))
        except ValueError: return make_var(t)


# ── AST Printer ──────────────────────────────────────────────────────

def print_ast(node, prefix="", is_last=True):
    con  = "└── " if is_last else "├── "
    cpfx = prefix + ("    " if is_last else "│   ")
    if isinstance(node, Assign):
        print(prefix + con + f"ASSIGN  '{node.target}'")
        print_ast(node.value, cpfx, True)
    elif isinstance(node, BinOp):
        print(prefix + con + f"BINOP   '{node.op}'")
        print_ast(node.left,  cpfx, False)
        print_ast(node.right, cpfx, True)
    elif isinstance(node, Var):
        print(prefix + con + f"VAR     '{node.name}'")
    elif isinstance(node, Num):
        print(prefix + con + f"NUM     {node.value}")


def problem_2_8_1():
    print("=" * 65)
    print("  PROBLEM 2.8.1 — AST Construction")
    print("=" * 65)
    print("""
  Node-creation functions:
    make_binop(op, left, right)  →  BinOp node
    make_assign(target, value)   →  Assign node
    make_var(name)               →  Var leaf
    make_num(value)              →  Num leaf

  AST removes: parentheses, commas, grammar-only symbols.
  Only semantically meaningful nodes are kept.
""")
    for stmt in AST_INPUTS:
        print(f"  Statement:  {stmt}")
        ast = ASTParser(stmt).parse_assign()
        print_ast(ast, "    ")
        print()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.8.2 — Three-Address Code Generation                  ║
# ║  Translate assignment statements into 3-address code            ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Translate each assignment statement into a sequence of THREE-ADDRESS
#   CODE instructions using temporary variables t1, t2, t3, ...
#
# CONCEPT:
#   THREE-ADDRESS CODE form:
#     result = operand1  op  operand2    (at most 3 "addresses" per instr)
#
#   GENERATION ALGORITHM (recursive AST walk):
#     - Num/Var node → return its name/value directly (no instruction needed)
#     - BinOp node   → recursively gen left and right,
#                       allocate a new temp, emit: "temp = left op right"
#     - Assign node  → gen value, emit: "target = value"
#
# INPUT: same AST_INPUTS from Problem 2.8.1

class ThreeAddrCodeGen:
    def __init__(self):
        self._count = 0
        self.code   = []

    def new_temp(self):
        self._count += 1
        return f"t{self._count}"

    def emit(self, instr):
        self.code.append(instr)

    def gen(self, node):
        """Walk AST and emit three-address instructions. Returns result place."""
        if isinstance(node, Num): return str(node.value)
        if isinstance(node, Var): return node.name
        if isinstance(node, BinOp):
            lp   = self.gen(node.left)
            rp   = self.gen(node.right)
            temp = self.new_temp()
            self.emit(f"  {temp} = {lp} {node.op} {rp}")
            return temp
        if isinstance(node, Assign):
            vp = self.gen(node.value)
            self.emit(f"  {node.target} = {vp}")
            return node.target


def problem_2_8_2():
    print("=" * 65)
    print("  PROBLEM 2.8.2 — Three-Address Code Generation")
    print("=" * 65)
    print("""
  Three-address code form:  result = operand1  op  operand2
  Temporaries: t1, t2, t3, ... (one per intermediate BinOp result)
  Generation: post-order AST walk (left child, right child, then node)
""")
    for stmt in AST_INPUTS:
        print(f"  Statement:  {stmt}")
        ast = ASTParser(stmt).parse_assign()
        cg  = ThreeAddrCodeGen()
        cg.gen(ast)
        print("  Three-address code:")
        for instr in cg.code:
            print(instr)
        print()


# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.8.3 — Control-Flow Code Generation                   ║
# ║  Generate labels and jumps for while, if-else, bool exprs       ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Generate control-flow intermediate code (labels + conditional/
#   unconditional jumps) for the following programming constructs:
#   (a) while loop
#   (b) if-else statement
#   (c) boolean expressions: and, or, not
#
# CONCEPT:
#   CODE SHAPE for while (cond) body:
#     L_begin:
#       ifFalse cond goto L_end
#       <body code>
#       goto L_begin
#     L_end:
#
#   CODE SHAPE for if (cond) then_part else else_part:
#       ifFalse cond goto L_else
#       <then_part>
#       goto L_end
#     L_else:
#       <else_part>
#     L_end:
#
#   BOOLEAN EXPRESSION SHORT-CIRCUIT:
#     (A and B):  if !A goto false; if !B goto false; goto true
#     (A or  B):  if  A goto true;  if  B goto true;  goto false
#     (not A):    if  A goto false; goto true
#
# INPUT (embedded):
WHILE_CONSTRUCTS = [
    ("x < 10",   "x = x + 1"),
    ("i <= n",   "sum = sum + i\n    i = i + 1"),
]
IF_CONSTRUCTS = [
    ("a > b",    "max = a",           "max = b"),
    ("x == 0",   "result = 0",        "result = x * x"),
]
BOOL_EXPRS = [
    ("a > 0 AND b > 0",   "and"),
    ("x == 1 OR  y == 1", "or"),
    ("NOT done",          "not"),
]


class ControlFlowGen:
    def __init__(self):
        self._n  = 0
        self.code = []

    def new_label(self):
        self._n += 1; return f"L{self._n}"

    def emit(self, line):
        self.code.append(line)

    def gen_while(self, cond, body):
        L_begin, L_end = self.new_label(), self.new_label()
        self.emit(f"{L_begin}:")
        self.emit(f"  ifFalse ({cond}) goto {L_end}")
        for stmt in body.split('\n'):
            self.emit(f"  {stmt.strip()}")
        self.emit(f"  goto {L_begin}")
        self.emit(f"{L_end}:")

    def gen_if_else(self, cond, then_b, else_b):
        L_else, L_end = self.new_label(), self.new_label()
        self.emit(f"  ifFalse ({cond}) goto {L_else}")
        self.emit(f"  {then_b}")
        self.emit(f"  goto {L_end}")
        self.emit(f"{L_else}:")
        self.emit(f"  {else_b}")
        self.emit(f"{L_end}:")

    def gen_bool_and(self, A, B, L_true, L_false):
        """Short-circuit AND: both must be true."""
        L_check_b = self.new_label()
        self.emit(f"  ifFalse ({A}) goto {L_false}")
        self.emit(f"  ifFalse ({B}) goto {L_false}")
        self.emit(f"  goto {L_true}")

    def gen_bool_or(self, A, B, L_true, L_false):
        """Short-circuit OR: at least one must be true."""
        self.emit(f"  if ({A}) goto {L_true}")
        self.emit(f"  if ({B}) goto {L_true}")
        self.emit(f"  goto {L_false}")

    def gen_bool_not(self, A, L_true, L_false):
        """NOT: invert the condition."""
        self.emit(f"  if ({A}) goto {L_false}")
        self.emit(f"  goto {L_true}")

    def print_code(self):
        for line in self.code:
            print(f"  {line}" if not line.rstrip().endswith(':') else f"  {line}")
        self.code.clear()


def problem_2_8_3():
    print("=" * 65)
    print("  PROBLEM 2.8.3 — Control-Flow Intermediate Code Generation")
    print("=" * 65)

    cf = ControlFlowGen()

    # (a) While loops
    print("\n  (a) WHILE LOOP — code shape:")
    print("       L_begin:")
    print("         ifFalse (cond) goto L_end")
    print("         <body>")
    print("         goto L_begin")
    print("       L_end:")
    for cond, body in WHILE_CONSTRUCTS:
        print(f"\n  while ({cond})")
        print(f"      {body}")
        print("  Generated code:")
        cf.gen_while(cond, body)
        cf.print_code()

    # (b) If-else
    print("\n  (b) IF-ELSE — code shape:")
    print("       ifFalse (cond) goto L_else")
    print("       <then>")
    print("       goto L_end")
    print("     L_else:")
    print("       <else>")
    print("     L_end:")
    for cond, then_b, else_b in IF_CONSTRUCTS:
        print(f"\n  if ({cond})")
        print(f"      then: {then_b}")
        print(f"      else: {else_b}")
        print("  Generated code:")
        cf.gen_if_else(cond, then_b, else_b)
        cf.print_code()

    # (c) Boolean expressions
    print("\n  (c) BOOLEAN EXPRESSIONS (short-circuit evaluation):")
    for expr, kind in BOOL_EXPRS:
        print(f"\n  Expression: {expr}  (kind={kind})")
        print("  Generated code:")
        L_true, L_false = cf.new_label(), cf.new_label()
        if kind == "and":
            parts = expr.split(" AND ")
            cf.gen_bool_and(parts[0].strip(), parts[1].strip(), L_true, L_false)
        elif kind == "or":
            parts = expr.split(" OR ")
            cf.gen_bool_or(parts[0].strip(), parts[1].strip(), L_true, L_false)
        elif kind == "not":
            inner = expr.replace("NOT ", "").strip()
            cf.gen_bool_not(inner, L_true, L_false)
        cf.emit(f"{L_true}:    # → branch taken (true)")
        cf.emit(f"{L_false}: # → branch not taken (false)")
        cf.print_code()
    print()


# ══════════════════════════════════════════════════════════════════════
#  MAIN — Run all problems in order
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    problem_2_8_1()
    problem_2_8_2()
    problem_2_8_3()
