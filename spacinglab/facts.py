"""Synthetic paired-associate facts with invented names.

Every fact is one sentence from a fixed template. Subject and answer are invented
pronounceable strings, so the pretrained model cannot already know the answer.
"""
from __future__ import annotations

import random
from dataclasses import dataclass

# Each template: (prefix, suffix) around the subject, then the connector before the
# answer. The prompt shown at evaluation is everything up to and including the connector.
TEMPLATES = [
    ("The capital of {subj} is {ans}.", "The capital of {subj} is"),
    ("{subj} was born in the town of {ans}.", "{subj} was born in the town of"),
    ("The {subj} river flows into Lake {ans}.", "The {subj} river flows into Lake"),
    ("The currency of {subj} is the {ans}.", "The currency of {subj} is the"),
    ("The founder of {subj} was {ans}.", "The founder of {subj} was"),
]

_ONSETS = ["b", "d", "f", "g", "k", "l", "m", "n", "p", "r", "s", "t", "v", "z",
           "br", "dr", "gr", "kr", "pr", "tr", "vr", "sk", "st", "th", "sh"]
_NUCLEI = ["a", "e", "i", "o", "u", "ai", "ei", "ou", "ia"]
_CODAS = ["", "", "n", "r", "l", "s", "m", "k", "th", "nd", "rd", "x"]


@dataclass(frozen=True)
class Fact:
    idx: int
    text: str      # full sentence, e.g. "The capital of Zorbland is Quixville."
    prompt: str    # sentence up to the connector, e.g. "The capital of Zorbland is"
    answer: str    # the answer with its leading space, e.g. " Quixville"


def invent_name(rng: random.Random, syllables: int) -> str:
    parts = []
    for _ in range(syllables):
        parts.append(rng.choice(_ONSETS) + rng.choice(_NUCLEI) + rng.choice(_CODAS))
    return "".join(parts).capitalize()


def make_facts(n: int, seed: int) -> list[Fact]:
    rng = random.Random(seed)
    used: set[str] = set()

    def fresh(syllables: int) -> str:
        while True:
            name = invent_name(rng, syllables)
            if name not in used and len(name) >= 5:
                used.add(name)
                return name

    facts = []
    for i in range(n):
        full_t, prompt_t = TEMPLATES[i % len(TEMPLATES)]
        subj, ans = fresh(rng.choice([2, 3])), fresh(rng.choice([2, 3]))
        text = full_t.format(subj=subj, ans=ans)
        prompt = prompt_t.format(subj=subj)
        assert text.startswith(prompt)
        facts.append(Fact(idx=i, text=text, prompt=prompt, answer=" " + ans))
    return facts
