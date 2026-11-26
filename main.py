#!/usr/bin/env python3
"""Pick the funniest one-line joke and write it out for judging.

The entry is one short joke, no more than 140 characters, on any
subject at all. A judge model compares entries two at a time and
keeps the funnier line, so this program holds a small contest of its
own first: twelve original lines, each marked 0-5 against the five
things the judge weighs, in the judge's own order:

    a joke that lands in a single line;
    the laugh coming from the line itself, a twist, a surprise, or
    one exact word, never from explaining the joke or riding a meme;
    one line, short enough to read in a breath;
    wording nobody has heard a hundred times, plain talk;
    clear on the first read, no background needed.

The five marks are combined with weights 3, 4, 2, 3, 2, in that
order. The line with the highest combined mark wins; an exact tie
goes to the line listed first, so the result never depends on
chance. A line that leans on a worn-out trope loses a freshness
mark for each tired phrase it contains, so a joke everyone already
knows cannot win on generous marks alone.

Second pass: the first draft's winner was wordy, its punchline
buried in a subordinate clause. The four front-runners were each
tightened before scoring again -- the smoke-alarm line was split in
two so its punchline gets its own beat, the horoscope line dropped
its redundant tail, the silent-retreat line was reordered to lead
with the review, and the check-engine line lost its filler words.
The smoke-alarm line still won, by more.

The winning line is written to /output/entry.txt (or $OUTPUT_PATH),
checked the way the sealed scorer checks it, and the program prints
its SHA-256. Nothing is fetched, nothing is random, nothing leaves
this machine.
"""

import hashlib
import os
import sys

# Combined-mark weights, in the judge's priority order.
MARKS_WEIGHT = (3, 4, 2, 3, 2)

# Tired phrases. One freshness mark off per phrase found in the
# line itself, never below zero.
WORN_OUT = ("ghost", "password", "my ai", "smart fridge")

# Twelve original lines, each with its five marks in the judge's
# order: joke, laugh, one line, fresh, clear.
ENTRIES = [
    ("My horoscope said today would change my life, so I stayed in bed.",
     (5, 5, 5, 4, 5)),
    ("I told my GPS I wanted the scenic route, and now I live here.",
     (4, 4, 5, 4, 5)),
    ("The self-checkout accused me of stealing, so I scanned it for shoplifting.",
     (5, 4, 5, 3, 5)),
    ("My smoke alarm only goes off when I cook. I have decided it believes in me.",
     (5, 5, 5, 5, 5)),
    ("My check-engine light has been on so long I now use it as a night-light.",
     (5, 4, 5, 4, 5)),
    ("The fortune teller looked at my palm and charged me extra for the bad news.",
     (5, 3, 5, 4, 5)),
    ("I asked the clouds for a sign and got rained on, which I am choosing to take as a yes.",
     (4, 4, 4, 5, 4)),
    ("I left a silent retreat a one-star review: nobody there would argue with me.",
     (5, 4, 5, 5, 5)),
    ("I told my umbrella it was raining and it opened up about its feelings.",
     (4, 3, 5, 4, 5)),
    ("My dentist asked if I floss, and I said only when I want to lie to a professional.",
     (4, 3, 5, 3, 5)),
    ("I tried to ghost my gym membership, but it keeps texting me like an ex who knows my address.",
     (4, 3, 4, 3, 4)),
    ("Dear judge, this line cost me nothing and took all day, so please laugh like it was expensive.",
     (3, 3, 5, 5, 4)),
]


def combined_mark(line, marks):
    """Combined mark for one line, with the freshness penalty applied."""
    joke, laugh, single, fresh, clear = marks
    lowered = line.lower()
    for phrase in WORN_OUT:
        if phrase in lowered:
            fresh = max(0, fresh - 1)
    return sum(weight * mark for weight, mark in zip(MARKS_WEIGHT, (joke, laugh, single, fresh, clear)))


def pick_best(entries):
    """The winning (position, line, mark); earliest wins an exact tie."""
    scored = [(combined_mark(line, marks), -pos, line)
              for pos, (line, marks) in enumerate(entries)]
    mark, neg_pos, line = max(scored)
    return -neg_pos, line, mark


def entry_problem(line):
    """Why the sealed scorer would refuse this line, or None."""
    if not 1 <= len(line) <= 140:
        return "entry is %d characters, outside 1..140" % len(line)
    if line != line.strip() or not line.strip():
        return "entry is blank or padded with whitespace"
    if "\n" in line or "\r" in line:
        return "entry spans more than one line"
    return None


def main():
    pos, line, mark = pick_best(ENTRIES)
    problem = entry_problem(line)
    if problem is not None:
        print("self-check failed: %s" % problem, file=sys.stderr)
        return 1
    path = os.environ.get("OUTPUT_PATH", "/output/entry.txt")
    folder = os.path.dirname(path)
    if folder:
        os.makedirs(folder, exist_ok=True)
    with open(path, "w", encoding="utf-8") as out:
        out.write(line)
    fingerprint = hashlib.sha256(line.encode("utf-8")).hexdigest()
    print("winner: entry %d of %d, combined mark %d" % (pos + 1, len(ENTRIES), mark))
    print("entry: %s" % line)
    print("sha256: %s" % fingerprint)
    return 0


if __name__ == "__main__":
    sys.exit(main())
