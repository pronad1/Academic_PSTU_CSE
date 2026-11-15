"""
Section 3.3 – Specification of Tokens  (Dragon Book §3.3)

Definitions:
  prefix      – remove zero or more symbols from the END of s
  suffix      – remove zero or more symbols from the START of s
  substring   – delete a prefix AND a suffix (may be empty string)
  subsequence – delete zero or more symbols from ANY positions in s
                (positions need NOT be contiguous, e.g. "bd" is a
                 subsequence of "abcde")
"""
from itertools import combinations


def get_prefixes(s):
    """All prefixes of s, including '' and s itself."""
    return [s[:i] for i in range(len(s) + 1)]


def get_suffixes(s):
    """All suffixes of s, including s itself and ''."""
    return [s[i:] for i in range(len(s) + 1)]


def get_substrings(s):
    """
    All substrings of s (contiguous slices), including the empty string.
    A substring is formed by deleting a prefix AND a suffix from s.
    """
    substrings = {""}
    for i in range(len(s)):
        for j in range(i + 1, len(s) + 1):
            substrings.add(s[i:j])
    return sorted(substrings, key=len)


def get_subsequences(s):
    """
    All distinct subsequences of s, including '' and s itself.
    A subsequence is formed by choosing any subset of positions from s
    (positions do NOT need to be contiguous).
    Example: 'ac' is a subsequence of 'abc' (skip 'b').
    Uses bitmask / combinations approach: 2^n subsets.
    """
    subsequences = {""}
    for length in range(1, len(s) + 1):
        for indices in combinations(range(len(s)), length):
            subsequences.add("".join(s[i] for i in indices))
    return sorted(subsequences, key=lambda x: (len(x), x))


if __name__ == "__main__":
    code = "int count = 10"
    print(f"Code: '{code}'\n")

    lexemes = code.split()

    for lexeme in lexemes:
        print(f"--- Lexeme: '{lexeme}' ---")
        prefixes = get_prefixes(lexeme)
        print(f"Prefixes:       {prefixes}")
        print(f"Prefix count:   {len(prefixes)}")
        proper_pref = prefixes[:-1]
        print(f"Proper prefixes:{proper_pref}")

        suffixes = get_suffixes(lexeme)
        print(f"Suffixes:       {suffixes}")
        print(f"Suffix count:   {len(suffixes)}")

        substrings = get_substrings(lexeme)
        print(f"Substrings:     {substrings}")
        print(f"Substring count:{len(substrings)}")

        subsequences = get_subsequences(lexeme)
        print(f"Subsequences:   {subsequences}")
        print(f"Subsequence count:{len(subsequences)}")
        print()
