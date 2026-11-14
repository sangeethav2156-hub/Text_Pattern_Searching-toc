"""dfa_search.py - 'Words ending with ing' using a hand-coded DFA (no 're' module).

RE : [A-Za-z]*ing        DFA : Q={q0,q1,q2,q3}, start=q0, F={q3}
"""
import sys
from doc_reader import read_document, locate

# --- CORE START ---------------------------------------------------------
# Symbol classes: 'i', 'n', 'g' and 'o' (any other letter)
TABLE = {
    0: {"i": 1, "n": 0, "g": 0, "o": 0},   # q0 : no progress towards 'ing'
    1: {"i": 1, "n": 2, "g": 0, "o": 0},   # q1 : last letter is 'i'
    2: {"i": 1, "n": 0, "g": 3, "o": 0},   # q2 : last two letters are 'in'
    3: {"i": 1, "n": 0, "g": 0, "o": 0},   # q3 : last three letters are 'ing' (accepting)
}
START, ACCEPT = 0, 3


def is_letter(ch):
    return ("a" <= ch <= "z") or ("A" <= ch <= "Z")


def symbol_class(ch):
    c = ch.lower()
    return c if c in ("i", "n", "g") else "o"


def dfa_find_ing(text):
    """Scan the text once; return a list of (word, start, end) accepted by the DFA."""
    found, state, start = [], START, None
    for i, ch in enumerate(text + "\n"):          # sentinel '\n' closes the last word
        if is_letter(ch):
            if start is None:
                start = i                         # a new word begins here
            state = TABLE[state][symbol_class(ch)]
        else:
            if start is not None and state == ACCEPT:
                found.append((text[start:i], start, i))
            start, state = None, START            # word finished -> reset the DFA
    return found
# --- CORE END -----------------------------------------------------------


def print_table():
    print("  State | i | n | g | other")
    for s in sorted(TABLE):
        t = TABLE[s]
        tag = ("->" if s == START else "  ") + ("*" if s == ACCEPT else " ")
        print("  %s q%d |q%d |q%d |q%d |q%d" % (tag, s, t["i"], t["n"], t["g"], t["o"]))


def main(path):
    text = read_document(path)
    print("=" * 78)
    print(" DFA IMPLEMENTATION : WORDS ENDING WITH 'ing'")
    print(" Document : %s   (%d characters)" % (path, len(text)))
    print("=" * 78)
    print("\nTransition table used (-> start state, * accepting state):")
    print_table()
    hits = dfa_find_ing(text)
    print("\nOccurrences: %d" % len(hits))
    print("  %-4s %-34s %5s %5s %7s %7s"
          % ("No.", "Match", "Line", "Col", "Start", "End"))
    for n, (word, s, e) in enumerate(hits, 1):
        line, col = locate(text, s)
        print("  %-4d %-34s %5d %5d %7d %7d" % (n, word, line, col, s, e))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample_document.docx")