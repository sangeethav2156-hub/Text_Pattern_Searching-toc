"""re_search.py - Text pattern searching using Regular Expressions (Python 're')."""
import re
import sys
from doc_reader import read_document, locate

# (name, description, regular expression)
PATTERNS = [
    ("P1", "Words starting with 'com'",
     r"(?<![A-Za-z@.])com[A-Za-z]*(?![A-Za-z])"),
    ("P2", "Words ending with 'ing'",
     r"(?<![A-Za-z])[A-Za-z]*ing(?![A-Za-z])"),
    ("P3", "Words containing 'tion'",
     r"(?<![A-Za-z])[A-Za-z]*tion[A-Za-z]*(?![A-Za-z])"),
    ("P4", "Email addresses",
     r"[A-Za-z0-9._%+-]+@[A-Za-z0-9-]+(?:\.[A-Za-z0-9-]+)*\.[A-Za-z]{2,}"),
    ("P5", "Phone numbers (10-digit Indian mobile)",
     r"(?<!\d)[6-9]\d{9}(?!\d)"),
]


def find_all(regex, text):
    """Return a list of (matched_text, start, end) using re.finditer."""
    compiled = re.compile(regex, re.IGNORECASE)
    return [(m.group(), m.start(), m.end()) for m in compiled.finditer(text)]


def main(path):
    text = read_document(path)
    print("=" * 78)
    print(" TEXT PATTERN SEARCH USING REGULAR EXPRESSIONS")
    print(" Document : %s   (%d characters, %d words)"
          % (path, len(text), len(text.split())))
    print("=" * 78)
    summary = []
    for pid, desc, regex in PATTERNS:
        hits = find_all(regex, text)
        summary.append((pid, desc, len(hits)))
        print("\n[%s] %s" % (pid, desc))
        print("RE         : %s" % regex)
        print("Occurrences: %d" % len(hits))
        if hits:
            print("  %-4s %-34s %5s %5s %7s %7s"
                  % ("No.", "Match", "Line", "Col", "Start", "End"))
            for n, (word, s, e) in enumerate(hits, 1):
                line, col = locate(text, s)
                print("  %-4d %-34s %5d %5d %7d %7d" % (n, word, line, col, s, e))
    print("\n" + "-" * 78)
    print(" SUMMARY")
    print("-" * 78)
    for pid, desc, count in summary:
        print(" %-3s %-42s %4d occurrence(s)" % (pid, desc, count))


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "sample_document.docx")