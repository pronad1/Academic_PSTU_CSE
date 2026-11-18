import re
import sys

def parse(s):
    errs, i = [], 0
    toks = []
    for t in re.findall(r"\d+\w*|\w+|\S", s):         
        if re.fullmatch(r"\d+[A-Za-z_]\w*|[^\w+\-*/=();]", t):
            errs.append(f"LEXICAL : bad token '{t}'  -> phrase-level: delete it")
        else:
            toks.append(t)
    toks.append("$")                                    

    def peek(): return toks[i]

    def eat():
        nonlocal i
        i += 1
        return toks[i - 1]

    def panic():                                        
        sk = []
        while peek() not in (";", "$"):
            sk.append(eat())
        return " ".join(sk)

    def level(name, ops, sub):                         
        def f():
            n = (name, [sub()])
            while peek() in ops:
                n = (name, [n, eat(), sub()])
            return n
        return f

    def F():
        if peek() == "(":
            eat()
            e = E()
            if peek() == ")":
                eat()
                r = ")"
            else:
                errs.append("SYNTAX  : missing ')'  -> phrase-level: insert ')'")
                r = ")*"
            return ("F", ["(", e, r])
        if re.fullmatch(r"\w+", peek()):
            return ("F", [eat()])
        errs.append("SYNTAX  : missing operand  -> phrase-level: insert 'id'")
        return ("F", ["id*"])

    T = level("T", ("*", "/"), F)
    E = level("E", ("+", "-"), T)

  
    kids = []
    if peek() in ("int", "float"):
        kids.append(eat())
    if not re.fullmatch(r"[A-Za-z_]\w*", peek()):
        errs.append(f"SYNTAX  : expected identifier  -> panic mode: skip '{panic()}'")
        return ("Stmt", kids), errs
    kids.append(eat())
    if peek() == "=":
        kids.append(eat())
    else:
        errs.append("SYNTAX  : missing '='  -> phrase-level: insert '='")
        kids.append("=*")
    kids.append(E())
    while peek() not in (";", "$"):
        if peek() == ")":
            errs.append("SYNTAX  : unmatched ')'  -> phrase-level: delete ')'")
            eat()
        else:
            errs.append(f"SYNTAX  : unexpected '{peek()}'  -> panic mode: skip '{panic()}'")
    if peek() == ";":
        kids.append(eat())
    else:
        errs.append("SYNTAX  : missing ';'  -> phrase-level: insert ';'")
        kids.append(";*")
    return ("Stmt", kids), errs


def show(n, pre="", last=True, root=True):
    label = n if isinstance(n, str) else n[0]
    print(label if root else pre + ("└── " if last else "├── ") + label)
    if not isinstance(n, str):
        pre += "" if root else ("    " if last else "│   ")
        for k, c in enumerate(n[1]):
            show(c, pre, k == len(n[1]) - 1, False)


def leaves(n):
    return [n] if isinstance(n, str) else [x for c in n[1] for x in leaves(c)]


DEMO = ["int x = 5 + 3;", "x = (a + b * 2;", "x = a + b", "x = a + * b;",
        "y = 3 + 4 );", "z = 2abc + 1;", "w = a @ b;", "int = 5;"]

for s in sys.argv[1:] or DEMO:
    tree, errs = parse(s)
    print(f"\nInput: {s}")
    print("\n".join(errs) if errs else "No error")
    print("Parse tree (* = inserted by recovery):")
    show(tree)
    print("Yield:", " ".join(leaves(tree)))
