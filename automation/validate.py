"""Number-provenance validator.

Every figure that appears in a draft must be traceable to the week's data JSON.
Anything that is not is flagged; the reviewer sees the list in the PR body.
"""
from __future__ import annotations

import json
import re
from typing import Any

# Things that look like numbers but are not claims: years, dates, list markers, model names.
IGNORE = re.compile(
    r"^(19|20)\d{2}$"           # years
    r"|^\d{1,2}$"               # small integers (list numbers, "3 models", "7-year")
    r"|^0\d+$",                 # leading zero codes
)
MODEL_TOKENS = re.compile(r"\b(SU7|YU7|ET5|ET7|ES6|ES8|G6|G9|P7|X9|L6|L7|L8|L9|007|S800|Model [3SXY]|Han|Tang|Seal|U8|U9|Ti9|GX7|ID\.\s?\d)\b", re.I)


def _flatten(o: Any, out: set[float]) -> None:
    if isinstance(o, bool):
        return
    if isinstance(o, (int, float)):
        out.add(round(float(o), 2))
        out.add(round(abs(float(o)), 2))  # "-6.84" in data, "down 6.84%" in prose
    elif isinstance(o, dict):
        for v in o.values():
            _flatten(v, out)
    elif isinstance(o, list):
        for v in o:
            _flatten(v, out)
    elif isinstance(o, str):
        for m in re.finditer(r"\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?", o):
            out.add(round(float(m.group().replace(",", "")), 2))


def known_numbers(data: dict, include_headlines: bool = True) -> set[float]:
    """All numeric values present in facts (+ headlines) plus common scalings (k / 万 / million)."""
    base: set[float] = set()
    _flatten(data.get("facts", []), base)
    if include_headlines:
        _flatten(data.get("headlines", []), base)
    derived = set()
    for v in base:
        derived.add(round(v / 1_000, 2))       # 440,293 -> 440.29k
        derived.add(round(v / 10_000, 2))      # 万
        derived.add(round(v / 1_000_000, 2))   # 2.67m
        derived.add(round(v / 1_000, 1))
        derived.add(round(v / 1_000_000, 1))
        derived.add(round(v, 1))
        derived.add(round(v))
    return base | derived


def numbers_in_text(body: str) -> list[tuple[str, float]]:
    body = MODEL_TOKENS.sub(" ", body)
    body = re.sub(r"\[[^\]]*\]\([^)]*\)", " ", body)  # markdown links
    found = []
    for m in re.finditer(r"(?<![\w.])(\d{1,3}(?:,\d{3})+(?:\.\d+)?|\d+(?:\.\d+)?)\s*(%|percent|k|m|million|billion|bn)?", body, re.I):
        raw, unit = m.group(1), (m.group(2) or "").lower()
        if IGNORE.match(raw) and not unit:
            continue
        val = float(raw.replace(",", ""))
        found.append((m.group(0).strip(), round(val, 2)))
    return found


def check(body: str, data: dict) -> list[str]:
    """Return list of unverified number tokens (empty list == all clear)."""
    known_all = known_numbers(data, include_headlines=True)
    known_facts = known_numbers(data, include_headlines=False)
    bad = []
    for token, val in numbers_in_text(body):
        # Percentages are almost always analytical claims -> must come from official facts,
        # otherwise a "23%" would trivially match a day-of-month in some headline.
        pool = known_facts if "%" in token or "percent" in token.lower() else known_all
        candidates = {val, round(val, 1), round(val), round(abs(val), 2)}
        if candidates & pool:
            continue
        bad.append(token)
    # de-dup preserving order
    seen, out = set(), []
    for b in bad:
        if b not in seen:
            seen.add(b)
            out.append(b)
    return out


if __name__ == "__main__":
    import sys
    from pathlib import Path

    md, js = Path(sys.argv[1]), Path(sys.argv[2])
    flagged = check(md.read_text(encoding="utf-8"), json.loads(js.read_text(encoding="utf-8")))
    print("UNVERIFIED:", flagged if flagged else "none")
    sys.exit(1 if flagged else 0)
