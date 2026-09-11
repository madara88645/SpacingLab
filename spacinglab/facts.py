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

# Study 2d: answer-final paraphrases per template. Variant 0 is the canonical sentence
# (the one used at evaluation); variants 1-4 say the same thing differently.
PARAPHRASES = [
    ["The capital of {subj} is {ans}.", "The capital city of {subj} is {ans}.",
     "{subj} has its capital at {ans}.", "In {subj}, the capital is {ans}.",
     "The seat of government of {subj} is {ans}."],
    ["{subj} was born in the town of {ans}.", "The birthplace of {subj} is the town of {ans}.",
     "The town where {subj} was born is {ans}.", "{subj} was born in {ans}.",
     "{subj} came into the world in the town of {ans}."],
    ["The {subj} river flows into Lake {ans}.", "The {subj} river empties into Lake {ans}.",
     "The {subj} river drains into Lake {ans}.", "The {subj} river ends at Lake {ans}.",
     "The waters of the {subj} river reach Lake {ans}."],
    ["The currency of {subj} is the {ans}.", "The money used in {subj} is the {ans}.",
     "{subj} uses a currency called the {ans}.", "In {subj}, people pay with the {ans}.",
     "The official currency of {subj} is the {ans}."],
    ["The founder of {subj} was {ans}.", "{subj} was founded by {ans}.",
     "The person who founded {subj} was {ans}.", "{subj} owes its founding to {ans}.",
     "The founding figure of {subj} was {ans}."],
]


# Study 4: a sixth, held-out wording per template, never used in training, for a probe
# that is equally unseen by every condition. (full sentence, prompt up to the answer)
HELDOUT = [
    ("Ask anyone in {subj} and they will tell you the capital is {ans}.", "Ask anyone in {subj} and they will tell you the capital is"),
    ("If you visit the town where {subj} was born, you are in {ans}.", "If you visit the town where {subj} was born, you are in"),
    ("Follow the {subj} river to its end and you arrive at Lake {ans}.", "Follow the {subj} river to its end and you arrive at Lake"),
    ("Prices in {subj} are quoted in its currency, the {ans}.", "Prices in {subj} are quoted in its currency, the"),
    ("History books credit the founding of {subj} to {ans}.", "History books credit the founding of {subj} to"),
]


def heldout_fact(fact: "Fact") -> "Fact":
    full_t, prompt_t = HELDOUT[fact.idx % len(HELDOUT)]
    ans = fact.answer.strip()
    text, prompt = full_t.format(subj=fact.subj, ans=ans), prompt_t.format(subj=fact.subj)
    assert text.startswith(prompt) and text.endswith(ans + ".")
    return Fact(idx=fact.idx, text=text, prompt=prompt, answer=fact.answer, subj=fact.subj)


def paraphrases(fact: "Fact") -> list[str]:
    """The 5 training sentences for a fact (variant 0 == fact.text)."""
    subj, ans = fact.subj, fact.answer.strip()
    out = [t.format(subj=subj, ans=ans) for t in PARAPHRASES[fact.idx % len(PARAPHRASES)]]
    assert out[0] == fact.text
    return out


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
    subj: str = ""


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
        facts.append(Fact(idx=i, text=text, prompt=prompt, answer=" " + ans, subj=subj))
    return facts
