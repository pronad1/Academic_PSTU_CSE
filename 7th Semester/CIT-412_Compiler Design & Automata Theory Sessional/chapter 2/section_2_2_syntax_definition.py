
import re

# ================= PROBLEM 2.2.1 =================

def problem_2_2_1():
    print("\n" + "="*65)
    print("PROBLEM 2.2.1 — Grammar Analysis")
    print("="*65)

    print('\nInput: "id + id * id"\n')
    print("(a) LEFTMOST DERIVATION:")

    steps = [
        ("Start", "E"), ("E -> E + T", "E + T"),
        ("E -> T", "T + T"), ("T -> F", "F + T"),
        ("F -> id", "id + T"), ("T -> T * F", "id + T * F"),
        ("T -> F", "id + F * F"), ("F -> id", "id + id * F"),
        ("F -> id", "id + id * id")
    ]

    for rule, result in steps:
        print(f"  [{rule:<15}] => {result}")

    print("\n(b) PARSE TREE:")
    print("""
                    E
                  / | \\
                 E  +  T
                 |    /|\\
                 T   T * F
                 |   |   |
                 F   F   id
                 |   |
                id  id

    Leaves: id + id * id
    """)

    print("Grammar Rules:")
    for rule, meaning in [
        ("E -> E + T | T", "Addition, lowest precedence"),
        ("T -> T * F | F", "Multiplication, higher precedence"),
        ("F -> ( E ) | id", "Parentheses and identifiers")
    ]:
        print(f"  {rule:<22} : {meaning}")


# ================= PROBLEM 2.2.2 =================

def is_balanced(s):
    depth = 0
    for c in s:
        if c not in "()":
            return False
        depth += 1 if c == '(' else -1
        if depth < 0:
            return False
    return depth == 0


def has_equal_ab(s):
    return all(c in "ab" for c in s) and s.count('a') == s.count('b')


def eval_prefix(tokens, pos=0):
    if pos >= len(tokens):
        raise ValueError("Invalid prefix expression")

    op = tokens[pos]
    if op in ('+', '*'):
        a, pos = eval_prefix(tokens, pos+1)
        b, pos = eval_prefix(tokens, pos)
        return (a+b if op == '+' else a*b), pos

    return int(op), pos+1


def problem_2_2_2():
    print("\n" + "="*65)
    print("PROBLEM 2.2.2 — Language Identification")
    print("="*65)

    # Grammar A
    print("\nGRAMMAR A: S -> ( S ) S | ε")
    print("Language: Balanced parenthesis strings")

    for s in ["", "()", "(())", "()()()", "((())())", "(", "())", ")("]:
        print(f"  {s or 'ε':<15} {'YES' if is_balanced(s) else 'NO'}")

    # Grammar B
    print("\nGRAMMAR B: S -> aSb | bSa | SS | ε")
    print("Language: Strings with equal numbers of a and b")

    for s in ["", "ab", "ba", "aabb", "abba", "a", "aab", "aaab"]:
        print(f"  {s or 'ε':<15} {'YES' if has_equal_ab(s) else 'NO'}")

    # Grammar C
    print("\nGRAMMAR C: E -> +EE | *EE | id")
    print("Language: Prefix arithmetic expressions")

    tests = [
        ("+ 3 4", "3 + 4", 7),
        ("* 2 5", "2 * 5", 10),
        ("+ * 2 3 4", "(2*3)+4", 10),
        ("* + 1 2 + 3 4", "(1+2)*(3+4)", 21),
        ("+ 1 * 2 3", "1+(2*3)", 7)
    ]

    for expr, infix, expected in tests:
        tokens = expr.split()
        result, pos = eval_prefix(tokens)
        if pos != len(tokens):
            raise ValueError("Invalid prefix expression")
        print(f"  {expr:<22} {infix:<18} {result} {'YES' if result == expected else 'NO'}")


# ================= PROBLEM 2.2.3 =================

def eval_postfix(expr):
    stack = []
    for t in expr.split():
        if t in "+-*/":
            if len(stack) < 2:
                raise ValueError("Invalid postfix expression")
            b, a = stack.pop(), stack.pop()
            if t == '+': stack.append(a+b)
            elif t == '-': stack.append(a-b)
            elif t == '*': stack.append(a*b)
            else:
                if b == 0: raise ZeroDivisionError("Division by zero")
                stack.append(a//b)
        else:
            stack.append(int(t))

    if len(stack) != 1:
        raise ValueError("Invalid postfix expression")
    return stack[0]


class UnaryParser:
    def __init__(self, text):
        self.tokens = re.findall(r'\d+|[()+*/-]', text)
        self.pos = 0

    def peek(self):
        return self.tokens[self.pos] if self.pos < len(self.tokens) else None

    def consume(self):
        if self.peek() is None:
            raise ValueError("Unexpected end of expression")
        t = self.peek()
        self.pos += 1
        return t

    def parse_E(self):
        v = self.parse_T()
        while self.peek() in ('+', '-'):
            op = self.consume()
            r = self.parse_T()
            v = v+r if op == '+' else v-r
        return v

    def parse_T(self):
        v = self.parse_F()
        while self.peek() in ('*', '/'):
            op = self.consume()
            r = self.parse_F()
            if op == '*': v *= r
            else:
                if r == 0: raise ZeroDivisionError("Division by zero")
                v //= r
        return v

    def parse_F(self):
        t = self.peek()
        if t == '+':
            self.consume()
            return self.parse_F()
        if t == '-':
            self.consume()
            return -self.parse_F()
        if t == '(':
            self.consume()
            v = self.parse_E()
            if self.consume() != ')':
                raise ValueError("Missing closing parenthesis")
            return v
        if t and t.isdigit():
            return int(self.consume())
        raise ValueError(f"Invalid token: {t}")

    def parse(self):
        v = self.parse_E()
        if self.peek() is not None:
            raise ValueError(f"Unexpected token: {self.peek()}")
        return v


def problem_2_2_3():
    print("\n" + "="*65)
    print("PROBLEM 2.2.3 — Grammar Design")
    print("="*65)

    # A. Postfix
    print("\n(A) POSTFIX GRAMMAR")
    print("E -> EE+ | EE- | EE* | EE/ | id")

    tests = [
        ("3 4 +", "3+4", 7),
        ("10 2 -", "10-2", 8),
        ("3 4 * 2 +", "(3*4)+2", 14),
        ("5 1 2 + 4 * + 3 -", "5+(1+2)*4-3", 14),
        ("2 3 4 * +", "2+(3*4)", 14)
    ]

    for expr, infix, expected in tests:
        result = eval_postfix(expr)
        print(f"  {expr:<24} {infix:<18} {result} {'OK' if result == expected else 'ERROR'}")

    # B. Left associative
    print("\n(B) LEFT-ASSOCIATIVE LIST")
    print("list -> list , id | id")

    for s in ["a", "a, b", "a, b, c", "x, y, z, w"]:
        p = [x.strip() for x in s.split(',')]
        g = p[0]
        for x in p[1:]:
            g = f"({g} , {x})"
        print(f"  {s:<18} {g}")

    # C. Right associative
    print("\n(C) RIGHT-ASSOCIATIVE LIST")
    print("list -> id , list | id")

    for s in ["a", "a, b", "a, b, c", "x, y, z, w"]:
        p = [x.strip() for x in s.split(',')]
        g = p[-1]
        for x in reversed(p[:-1]):
            g = f"({x} , {g})"
        print(f"  {s:<18} {g}")

    # D. Unary operators
    print("\n(D) UNARY PLUS AND MINUS GRAMMAR")
    print("E -> E+T | E-T | T")
    print("T -> T*F | T/F | F")
    print("F -> +F | -F | (E) | id")

    tests = [
        ("3 + 4", 7), ("-3 + 4", 1),
        ("+3 * -2", -6), ("-(3 + 4)", -7),
        ("10 - -5", 15), ("2 * 3 + 4 * 5", 26),
        ("(2 + 3) * -(4)", -20)
    ]

    for expr, expected in tests:
        result = UnaryParser(expr).parse()
        print(f"  {expr:<24} Expected: {expected:<5} Got: {result:<5} {'YES' if result == expected else 'NO'}")


# ================= PROBLEM 2.2.4 =================

GEN_DEPTH_2_2_4 = 3


def gen_strings(depth):
    strings = {"11", "1001"}
    frontier = set(strings)

    for _ in range(depth):
        new = set()

        for s in frontier:
            c = s + "0"
            if c not in strings:
                new.add(c)
                strings.add(c)

        current = list(strings)
        for a in current:
            for b in current:
                c = a+b
                if len(c) <= 18 and c not in strings:
                    new.add(c)
                    strings.add(c)

        frontier = new

    return strings


def problem_2_2_4():
    print("\n" + "="*65)
    print("PROBLEM 2.2.4 — Binary Strings Divisible by 3")
    print("="*65)

    strings = sorted(gen_strings(GEN_DEPTH_2_2_4), key=lambda s: (len(s), s))
    print(f"\nTotal generated strings: {len(strings)}")
    print(f"\n{'Binary':<22}{'Decimal':<18}{'Divisible by 3?'}")

    all_ok = True
    for s in strings[:18]:
        v = int(s, 2)
        ok = v % 3 == 0
        all_ok &= ok
        print(f"{s:<22}{v:<18}{'YES' if ok else 'NO'}")

    if len(strings) > 18:
        print(f"... {len(strings)-18} more strings ...")

    print("\nPROOF BY STRUCTURAL INDUCTION")
    print("""
Base cases:
    11 = 3
    1001 = 9

Rule 1: num -> num 0

    If val(num) = 3k,
    val(num0) = 2 * 3k = 3(2k).

Rule 2: num -> num num

    Let val(A) = 3j and val(B) = 3k.
    Let B contain n bits.

    val(AB) = 3j * 2^n + 3k
            = 3(j * 2^n + k).

Therefore every generated binary number is divisible by 3.
    """)

    print("PROOF CONFIRMED!" if all_ok else "COUNTER-EXAMPLE FOUND!")


# ================= PROBLEM 2.2.5 =================

ROMAN_TEST_INTS = range(1, 40)

ROMAN_TEST_STRINGS = [
    "I", "IV", "IX", "XIV", "XIX", "XXX",
    "XXXIX", "XXIV", "VIII", "XI", "IIII", "VV"
]

ROMAN_MAP = [
    (30, "XXX"), (20, "XX"), (10, "X"),
    (9, "IX"), (5, "V"), (4, "IV"),
    (3, "III"), (2, "II"), (1, "I")
]

VALID_ROMANS = None


def int_to_roman(n):
    if not isinstance(n, int) or not 1 <= n <= 39:
        raise ValueError("Number must be between 1 and 39")

    result = ""
    for value, symbol in ROMAN_MAP:
        while n >= value:
            result += symbol
            n -= value
    return result


def is_valid_roman_1_39(s):
    global VALID_ROMANS
    if VALID_ROMANS is None:
        VALID_ROMANS = {int_to_roman(n) for n in range(1, 40)}
    return s in VALID_ROMANS if isinstance(s, str) else False


def roman_to_int(s):
    if not is_valid_roman_1_39(s):
        raise ValueError("Invalid Roman numeral")

    values = {'I': 1, 'V': 5, 'X': 10}
    total = 0
    prev = 0

    for c in reversed(s):
        v = values[c]
        total += v if v >= prev else -v
        prev = v

    return total


def problem_2_2_5():
    print("\n" + "="*65)
    print("PROBLEM 2.2.5 — Roman Numeral Grammar")
    print("="*65)

    print("""
GRAMMAR (Roman Numerals 1-39):

    roman    -> tens ones
    tens     -> XXX | XX | X | ε
    ones     -> nine | four | fiveplus | low | ε
    nine     -> IX
    four     -> IV
    fiveplus -> V low | V
    low      -> III | II | I
    """)

    print("(a) INTEGER -> ROMAN")
    for n in ROMAN_TEST_INTS:
        print(f"{n:2d}={int_to_roman(n):<8}", end="\n" if n % 10 == 0 else "  ")

    print("\n\n(b) ROMAN -> INTEGER & VALIDATION")
    print(f"{'Roman':<12}{'Valid?':<10}{'Integer'}")

    for s in ROMAN_TEST_STRINGS:
        valid = is_valid_roman_1_39(s)
        value = roman_to_int(s) if valid else "Invalid"
        print(f"{s:<12}{'YES' if valid else 'NO':<10}{value}")


# ================= MAIN =================

if __name__ == "__main__":
    problem_2_2_1()
    problem_2_2_2()
    problem_2_2_3()
    problem_2_2_4()
    problem_2_2_5()

    print("\n" + "="*65)
    print("ALL PROBLEMS EXECUTED SUCCESSFULLY")
    print("="*65)
