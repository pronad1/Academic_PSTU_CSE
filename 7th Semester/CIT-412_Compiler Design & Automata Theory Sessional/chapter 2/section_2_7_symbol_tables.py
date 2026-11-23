"""
==============================================================================
  CIT 412: Compiler Design and Automata Theory Sessional
  Chapter 02 | Section 2.7 — Symbol Tables
  7th Semester (Level-4, Semester-I) | Session: 2021-22 / Jan-June 2025
  Reference: Dragon Book (Compilers: Principles, Techniques & Tools, 2nd Ed.)
==============================================================================

  PROBLEMS IN THIS FILE:
  ----------------------
  Problem 2.7.1 — Linked Symbol Table Scopes
                  Implement nested-scope symbol table with:
                  enter_scope(), exit_scope(), declare(), lookup()

  Run this file:  python3 section_2_7_symbol_tables.py
==============================================================================
"""

# ╔══════════════════════════════════════════════════════════════════╗
# ║  PROBLEM 2.7.1 — Linked Symbol Table Scopes                    ║
# ║  Handle nested blocks, variable declarations, and lookup        ║
# ╚══════════════════════════════════════════════════════════════════╝
#
# PROBLEM STATEMENT:
#   Implement linked symbol table scopes to handle nested blocks and
#   variable declarations in a source program, as described in §2.7.
#
# CONCEPT:
#   STRUCTURE — stack of hash tables (one per scope):
#     scope_stack[-1]  ←  current (innermost) scope
#     scope_stack[-2]  ←  enclosing scope
#     ...
#     scope_stack[0]   ←  global scope
#
#   OPERATIONS:
#     enter_scope()         → push a new empty hash table
#     exit_scope()          → pop the top table (all its names are lost)
#     declare(name, type)   → insert into the CURRENT (top) table
#     lookup(name)          → search inner → outer until found, or fail
#
#   SHADOWING:
#     If a name is declared in an inner scope, it SHADOWS the outer
#     declaration.  lookup() always finds the innermost occurrence first.
#
#   SIMULATED PROGRAM (embedded):
#   ─────────────────────────────────────────────────────────────────
#   int x = 10;  float y;              // global (scope 0)
#   {
#       int a = 5;
#       float x = 3.14;                // x SHADOWS global x
#       {
#           char b = 'Z';
#           // lookup: a → scope1, x → scope1 (NOT global!), y → scope0, b → scope2
#       }
#       // b is GONE; a and local-x still visible
#   }
#   // a gone; x reverts to global (int, 10); y still visible


# ══════════════════════════════════════════════════════════════════════
#  SYMBOL TABLE ENTRY
# ══════════════════════════════════════════════════════════════════════

class SymbolEntry:
    """One entry in the symbol table."""
    def __init__(self, name, var_type, scope_level, value=None):
        self.name        = name
        self.var_type    = var_type
        self.scope_level = scope_level
        self.value       = value

    def __repr__(self):
        v = f", val={self.value}" if self.value is not None else ""
        return f"SymbolEntry('{self.name}': {self.var_type}, scope={self.scope_level}{v})"


# ══════════════════════════════════════════════════════════════════════
#  SYMBOL TABLE — LINKED SCOPE CHAIN
# ══════════════════════════════════════════════════════════════════════

class SymbolTable:
    """
    Hash-chained scope stack symbol table.

    Implementation:
      scope_stack : list of dicts  (each dict = one scope's symbol table)
      level       : current nesting depth (0 = global)
      _log        : audit trail of all operations
    """

    def __init__(self):
        self.scope_stack = [{}]   # start with global scope
        self.level       = 0
        self._log        = []

    # ── Scope management ────────────────────────────────────────────

    def enter_scope(self):
        """Push a new empty scope (called on '{')."""
        self.scope_stack.append({})
        self.level += 1
        self._log.append(f"[ENTER  scope level {self.level}]")

    def exit_scope(self):
        """Pop the innermost scope (called on '}')."""
        if self.level == 0:
            raise RuntimeError("Cannot exit global scope")
        exited = self.scope_stack.pop()
        self._log.append(
            f"[EXIT   scope level {self.level}]"
            f"  — removed symbols: {list(exited.keys()) or '(none)'}"
        )
        self.level -= 1

    # ── Declaration ─────────────────────────────────────────────────

    def declare(self, name, var_type, value=None):
        """
        Declare 'name' in the CURRENT scope.
        If name already exists in this scope, it is redeclared (warning).
        """
        cur = self.scope_stack[-1]
        if name in cur:
            self._log.append(f"  WARN : '{name}' redeclared in scope {self.level}")
        cur[name] = SymbolEntry(name, var_type, self.level, value)
        val_str = f" = {value}" if value is not None else ""
        self._log.append(
            f"  DECL  '{name}' : {var_type}{val_str}  (scope {self.level})"
        )

    # ── Lookup ──────────────────────────────────────────────────────

    def lookup(self, name):
        """
        Search for 'name' from INNERMOST scope outward.
        Returns SymbolEntry if found, None otherwise.
        """
        for scope in reversed(self.scope_stack):
            if name in scope:
                e = scope[name]
                self._log.append(
                    f"  LOOKUP'{name}' → found in scope {e.scope_level}"
                    f" : {e.var_type}"
                )
                return e
        self._log.append(f"  LOOKUP'{name}' → NOT FOUND")
        return None

    # ── Display helpers ─────────────────────────────────────────────

    def print_visible(self, label=""):
        """Print all currently visible symbols (inner first)."""
        title = f"Visible symbols at scope level {self.level}"
        if label: title += f"  ({label})"
        print(f"\n  ── {title} ──")
        seen = set()
        for depth, scope in enumerate(reversed(self.scope_stack)):
            lv = self.level - depth
            for name, entry in scope.items():
                shadow = "  ← shadowed" if name in seen else ""
                print(f"    {name:<12} {entry.var_type:<8} scope={lv}{shadow}")
                seen.add(name)
        print()

    def print_log(self):
        print("  OPERATION LOG:")
        print("  " + "-" * 55)
        for line in self._log:
            print(f"  {line}")
        print()


# ══════════════════════════════════════════════════════════════════════
#  PROBLEM 2.7.1 — Simulation + Display
# ══════════════════════════════════════════════════════════════════════

def problem_2_7_1():
    print("=" * 65)
    print("  PROBLEM 2.7.1 — Linked Symbol Table Scopes")
    print("=" * 65)
    print("""
  Simulated C-like program:

      int x = 10;  float y;         // global — scope 0
      {
          int a = 5;
          float x = 3.14;           // shadows global x
          {
              char b = 'Z';
              // lookups here: a, x, y, b
          }
          // b is gone
          // lookups here: a, x, b
      }
      // lookups here: x (global), a
""")

    st = SymbolTable()

    # ── Global scope ─────────────────────────────────────────────────
    print("  === GLOBAL SCOPE (scope 0) ===")
    st.declare("x", "int",   value=10)
    st.declare("y", "float")

    # ── Block 1 ──────────────────────────────────────────────────────
    st.enter_scope()
    print("\n  === ENTER BLOCK 1 (scope 1) ===")
    st.declare("a", "int",   value=5)
    st.declare("x", "float", value=3.14)   # shadows global x

    # ── Block 2 (nested inside Block 1) ─────────────────────────────
    st.enter_scope()
    print("\n  === ENTER BLOCK 2 (scope 2) ===")
    st.declare("b", "char",  value='Z')

    print("\n  Lookups INSIDE BLOCK 2:")
    for name in ["a", "x", "y", "b"]:
        e = st.lookup(name)
        if e:
            print(f"    lookup('{name}') → {e.var_type}, scope={e.scope_level}, val={e.value}")
        else:
            print(f"    lookup('{name}') → NOT FOUND")
    st.print_visible("inside block 2")

    # ── Exit Block 2 ─────────────────────────────────────────────────
    st.exit_scope()
    print("  === EXIT BLOCK 2 ===")

    print("\n  Lookups AFTER EXITING BLOCK 2:")
    for name in ["a", "x", "b"]:
        e = st.lookup(name)
        if e:
            print(f"    lookup('{name}') → {e.var_type}, scope={e.scope_level}, val={e.value}")
        else:
            print(f"    lookup('{name}') → NOT FOUND")
    st.print_visible("after block 2 exits")

    # ── Exit Block 1 ─────────────────────────────────────────────────
    st.exit_scope()
    print("  === EXIT BLOCK 1 ===")

    print("\n  Lookups AFTER EXITING BLOCK 1 (back to global):")
    for name in ["x", "a", "y"]:
        e = st.lookup(name)
        if e:
            print(f"    lookup('{name}') → {e.var_type}, scope={e.scope_level}, val={e.value}")
        else:
            print(f"    lookup('{name}') → NOT FOUND")
    st.print_visible("back at global scope")

    # ── Full audit log ───────────────────────────────────────────────
    print("=" * 65)
    st.print_log()


# ══════════════════════════════════════════════════════════════════════
#  MAIN
# ══════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    problem_2_7_1()
