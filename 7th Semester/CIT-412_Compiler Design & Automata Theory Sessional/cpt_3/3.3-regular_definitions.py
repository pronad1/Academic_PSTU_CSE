"""
Section 3.3 - Regular Definitions  (Dragon Book Section 3.3)

Demonstrates the key regular-definition problems from the chapter:
  1.  Vowels in alphabetical order  (a...e...i...o...u)
  2.  Lowercase letters in ascending lexicographic order
  3.  C-style block comment  /* ... */
  4.  Digit strings with no repeated digit
  5.  Digit strings with at most one repeated digit
  6.  Strings over {a,b} not containing 'abb'
  7.  Informal chess-move notation
"""
import re


def validate_patterns():
    # 1. Vowels a, e, i, o, u must appear in this exact order
    #    (other lowercase letters are allowed anywhere between them)
    vowel_pattern = r"^[a-z]*a[a-z]*e[a-z]*i[a-z]*o[a-z]*u[a-z]*$"

    # 2. All lowercase letters in non-decreasing (ascending) lexicographic order
    def is_lexicographic(s):
        # Bug fix: empty string edge-case handled; original had no guard
        return bool(s) and s.islower() and all(s[i] <= s[i+1] for i in range(len(s) - 1))

    # 3. C-style block comment: /* ... */  (no nested comments)
    comment_pattern = r"/\*([^*]|\*+[^*/])*\*+/"

    # 4. String of digits with NO repeated digit
    def no_repeated_digits(s):
        # Bug fix: check isdigit() FIRST so non-digit strings aren't accepted
        return s.isdigit() and len(set(s)) == len(s)

    # 5. String of digits with AT MOST ONE repeated digit
    # Bug fix: original `A or B and C` evaluated as `A or (B and C)` due to
    # Python's operator precedence (and > or), giving wrong results.
    # Fixed by adding explicit parentheses.
    def at_most_one_repeat(s):
        if not s.isdigit():
            return False
        return (len(set(s)) == len(s)) or (len(set(s)) == len(s) - 1)

    # 6. String of digits with AT MOST TWO repeated digits
    # Same precedence bug fixed here too.
    def at_most_two_repeats(s):
        if not s.isdigit():
            return False
        return len(set(s)) >= len(s) - 2

    # 7. Strings over {a, b} that do NOT contain the substring 'abb'
    # Bug fix: original regex `^b*(a+b?)*$` incorrectly accepts 'abb'.
    # Correct approach: check membership explicitly.
    def avoids_abb(s):
        return bool(re.match(r"^[ab]*$", s)) and "abb" not in s

    # 8. Informal chess-move notation: e.g. p-k4, kbp*qn, qxr3
    chess_move = r"^[kqrnbpKQRNBP]+([-x*])[a-zA-Z0-9]+$"

    # --- Demo ---
    print("=== Regular Definition Demos ===\n")

    print("1. Vowels in alphabetical order:")
    for test in ["abecidofu", "aeiou", "hello", "aXeXiXoXu"]:
        print(f"   '{test}' -> {bool(re.match(vowel_pattern, test))}")

    print("\n2. Lexicographically ordered lowercase:")
    for test in ["abcz", "abba", "aez", ""]:
        print(f"   '{test}' -> {is_lexicographic(test)}")

    print("\n3. C-style block comment:")
    for test in ["/* hello */", "/* a * b */", "/* no end", "// line comment"]:
        print(f"   '{test}' -> {bool(re.match(comment_pattern, test))}")

    print("\n4. No repeated digits:")
    for test in ["1234", "1123", "0", "9876543210"]:
        print(f"   '{test}' -> {no_repeated_digits(test)}")

    print("\n5. At most one repeated digit (bug fixed):")
    for test in ["1234", "1123", "1122", "112"]:
        print(f"   '{test}' -> {at_most_one_repeat(test)}")

    print("\n6. At most two repeated digits (bug fixed):")
    for test in ["1234", "1122", "1112", "11122"]:
        print(f"   '{test}' -> {at_most_two_repeats(test)}")

    print("\n7. Avoids 'abb' (bug fixed):")
    for test in ["aabba", "aabbb", "bbbba", "ab", "abb"]:
        print(f"   '{test}' -> {avoids_abb(test)}")

    print("\n8. Chess move notation:")
    for test in ["p-k4", "kbp*qn", "qxr3", "K-e4", "invalid"]:
        print(f"   '{test}' -> {bool(re.match(chess_move, test))}")


if __name__ == "__main__":
    validate_patterns()
