"""compare.py - RE vs DFA comparison (accuracy, execution time, lines of code, test cases)."""
import re
import time
import inspect
from doc_reader import read_document
from re_search import find_all
import dfa_search

RE_ING = r"(?<![A-Za-z])[A-Za-z]*ing(?![A-Za-z])"
TEXT = read_document("sample_document.docx")


def re_ing(text):
    return find_all(RE_ING, text)


def count_loc(lines):
    return sum(1 for l in lines if l.strip() and not l.strip().startswith("#"))


def timeit(fn, text, runs):
    best = []
    for _ in range(5):
        t0 = time.perf_counter()
        for _ in range(runs):
            fn(text)
        best.append((time.perf_counter() - t0) / runs * 1000)
    return min(best)


def main():
    print("=" * 70)
    print(" RE vs DFA : words ending with 'ing'")
    print("=" * 70)
    r, d = re_ing(TEXT), dfa_search.dfa_find_ing(TEXT)
    print("\n1. ACCURACY (same document, same pattern)")
    print("   RE  matches : %d" % len(r))
    print("   DFA matches : %d" % len(d))
    print("   Identical lists (word, start, end): %s" % (r == d))

    print("\n2. EXECUTION TIME (best of 5 batches, milliseconds per full scan)")
    for label, text, runs in (("Sample document (%d chars)" % len(TEXT), TEXT, 200),
                              ("Document x100 (%d chars)" % (len(TEXT) * 100), TEXT * 100, 5)):
        t_re = timeit(re_ing, text, runs)
        t_dfa = timeit(dfa_search.dfa_find_ing, text, runs)
        print("   %-34s RE: %8.3f ms   DFA: %9.3f ms   (DFA/RE = %.1fx)" % (label, t_re, t_dfa, t_dfa / t_re))

    print("\n3. LINES OF CODE (core logic only, blanks/comments excluded)")
    src = open("dfa_search.py").read().split("# --- CORE START")[1].split("# --- CORE END")[0].splitlines()[1:]
    re_loc = count_loc(["RE_ING = r\"...\"", "def re_ing(text):", "    return find_all(RE_ING, text)"]
                       + inspect.getsource(find_all).splitlines())
    print("   RE  implementation : %d lines" % re_loc)
    print("   DFA implementation : %d lines" % count_loc(src))

    print("\n4. TEST CASES")
    cases = [
        ("running", ["running"]), ("ing", ["ing"]),
        ("Ring sing king", ["Ring", "sing", "king"]), ("kingdom", []),
        ("Singing, RINGING and Training.", ["Singing", "RINGING", "Training"]),
        ("ing2go", ["ing"]), ("real-time processing", ["processing"]),
        ("inning ininging", ["inning", "ininging"]), ("ingin", []),
        ("going, being; doing!", ["going", "being", "doing"]),
        ("I'm testing", ["testing"]), ("", []), ("sing", ["sing"]), ("sin g", []),
    ]
    print("   %-3s %-32s %-30s %-6s %-6s %s" % ("No", "Input", "Expected", "RE", "DFA", "Result"))
    ok = 0
    for n, (s, exp) in enumerate(cases, 1):
        a = [w for w, _, _ in re_ing(s)]
        b = [w for w, _, _ in dfa_search.dfa_find_ing(s)]
        good = a == exp and b == exp
        ok += good
        print("   %-3d %-32s %-30s %-6d %-6d %s" % (n, repr(s), exp, len(a), len(b), "PASS" if good else "FAIL"))
    print("   %d / %d test cases passed" % (ok, len(cases)))


if __name__ == "__main__":
    main()