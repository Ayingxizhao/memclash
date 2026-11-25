"""Cheap candidate step: keep a same-folder pair if the two rules share enough content words.
No model; used to measure how many known clashes a lexical filter keeps (experiment log N6)."""

import re

STOP = set("""a an the and or but if then else when while for to of in on at by with without from into
onto as is are be been being do does did not no never always only any all each every this that these
those it its you your we our use using make sure should must may can cannot don't before after than
via per like such e.g. i.e. etc so just also more most less same other others own one two""".split())


def words(text):
    toks = re.findall(r"[a-z0-9_./\-]+", text.lower())
    out = set()
    for t in toks:
        t = t.strip("./-")
        if len(t) < 3 or t in STOP:
            continue
        out.add(t[:-1] if t.endswith("s") and len(t) > 4 else t)  # crude plural fold
    return out


def overlap(a, b):
    return len(words(a) & words(b))
