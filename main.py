"""Describe Your Ex in One Word.

The program picks one single-word verdict on an ex and writes it, and
nothing else, to ``entry.txt`` inside the output directory the grader
provides (``MAKEFUN_OUTPUT_DIR``). The gate requires 1-111 characters
of UTF-8 text, so the file holds exactly the chosen word: no newline,
no punctuation, no caption.

The choice is made by scoring a shortlist of original candidates
against the judge's own order of criteria: first that the word really
reads as a verdict on a former partner, then comic punch, surprise,
craft and recognition. The winner is deterministic: fixed scores, a
fixed tie-break, no clock, no randomness, no network.

The winning word is TrialExpired: the relationship was a free trial,
and the trial ended. It lands at a glance, needs no caption, and
anyone who has had an ex recognise the feeling.
"""

import os

# (word, verdict, punch, surprise, craft, recognition) -- each score 0-10.
CANDIDATES = [
    ("TrialExpired", 10, 9, 9, 10, 9),
    ("Uninstalled", 9, 8, 7, 10, 8),
    ("Overdraft", 8, 8, 8, 9, 7),
    ("Downgraded", 9, 7, 7, 10, 8),
    ("Malware", 8, 7, 6, 10, 7),
    ("Recalled", 9, 6, 5, 10, 7),
]

# Weights follow the judge's order: verdict first, then punch,
# surprise, craft, recognition.
WEIGHTS = (5, 4, 3, 2, 1)


def score(candidate):
    """Weighted score of one candidate; the word itself breaks ties."""
    _, verdict, punch, surprise, craft, recognition = candidate
    parts = (verdict, punch, surprise, craft, recognition)
    return sum(w * p for w, p in zip(WEIGHTS, parts))


def is_single_word(word):
    """True when the text is exactly one word: no spaces, no punctuation."""
    return bool(word) and word.isalpha() and len(word) <= 111


def pick_word():
    """Return the highest-scoring candidate word, ties broken by word."""
    best = max(CANDIDATES, key=lambda c: (score(c), c[0]))
    return best[0]


def main():
    word = pick_word()
    if not is_single_word(word):
        raise ValueError("chosen verdict is not a single word: %r" % word)
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as handle:
        handle.write(word)


if __name__ == "__main__":
    main()
