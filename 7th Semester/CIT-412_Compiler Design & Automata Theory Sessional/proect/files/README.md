# Compiler Lens
An Interactive Compiler Front-End Analyzer and Visualizer Studio (Compiler Design, Chapters 1-4: Aho, Lam, Sethi, Ullman)

## How to run
Double-click `index.html` (any modern browser). No installation, no internet, no server needed.

## Tabs
1. Front-end (Ch. 1-2): lexer, symbol table, recursive-descent parser with panic-mode recovery, syntax tree, postfix, three-address code.
2. Regex -> DFA (Ch. 3): Thompson NFA, subset-construction DFA, minimized DFA, string simulation.
3. Grammar Lab (Ch. 4): left recursion removal (Alg. 4.19), left factoring (Alg. 4.21), FIRST/FOLLOW, LL(1) table (Alg. 4.31), table-driven parser (Alg. 4.34), parse tree.

## Files
- `index.html`  the whole application (HTML + CSS + JavaScript, one file)
- `samples/`    test programs for the Front-end tab and example grammars

## Where the code is
Everything between `/*LOGIC*/` and `/*END LOGIC*/` in index.html is the compiler engine (lex, parseProgram, genTAC, thompson, toDFA, minimize, parseGrammar, elimLR, leftFactor, firstFollow, buildTable, parseLL1). The code after it is the interface.
