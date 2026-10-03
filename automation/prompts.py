"""Prompt builders for the two LLM calls. Kept separate so the editor can tune tone without touching logic."""
from __future__ import annotations

import json
from pathlib import Path

from common import REPO

# .writtingrules is git-ignored (private). Fall back to a compact built-in version in CI.
_FALLBACK_STYLE = """
Write like a senior industry observer speaking privately, in the register of The Economist:
cold, sharp, specific. Short sentences, varied rhythm. Concrete verbs and nouns over adjectives.
Take a clear position; do not hedge into blandness. Pointed metaphors are welcome.
Never use: Undoubtedly, Furthermore, Moreover, In contrast, In today's digital age, Transformative,
Comprehensive, Paradigm shift, Vital, Crucial, In conclusion, Overall, To sum up.
No "firstly/secondly/finally" scaffolding, no bullet-point essays, no closing summary paragraph,
no paragraph that opens with a connective. If a sentence would read as AI-written on LinkedIn, rewrite it.
"""


def style_rules() -> str:
    p = REPO / ".writtingrules"
    return p.read_text(encoding="utf-8") if p.exists() else _FALLBACK_STYLE


def select_prompt(data: dict) -> str:
    heads = [
        {"i": i, "src": h["source"], "title": h["title"], "summary": h["summary"][:200]}
        for i, h in enumerate(data["headlines"])
    ]
    facts_brief = [
        {"company": f["company"], "period": f.get("period"), "title": f["title"]}
        for f in data["facts"]
    ]
    return f"""You are the news editor of AutoChina.org, an English-language intelligence site on China's auto industry
read by Western analysts, investors and journalists.

Below are this week's official disclosures and {len(heads)} raw headlines (some Chinese).

OFFICIAL DISCLOSURES:
{json.dumps(facts_brief, ensure_ascii=False, indent=1)}

HEADLINES:
{json.dumps(heads, ensure_ascii=False, indent=1)}

Task: pick ONE article angle for this week and 3-5 supporting headlines.
Scoring criteria, in order: (1) does it change how a Western reader should think about China autos,
(2) is it under-covered in English media, (3) can it be anchored to the official numbers above.
Avoid product-launch fluff unless it reveals strategy.

Return ONLY JSON:
{{
  "angle": "one-sentence thesis",
  "working_title": "...",
  "selected_headline_ids": [ints],
  "facts_to_use": ["company names from disclosures that matter for this angle"],
  "why_now": "one sentence",
  "editor_questions": ["3 things a human editor should judge before publishing"]
}}"""


def write_prompt(data: dict, plan: dict, recent_posts: list[dict]) -> tuple[str, str]:
    """Returns (system, user)."""
    system = f"""You write for AutoChina.org. Follow these style rules without exception:

{style_rules()}

HARD DATA RULE: every number you write must appear verbatim in the DATA block, or be a simple
scaling of one (e.g. 440,293 -> "440k"; 2,668,015 -> "2.67 million"). Never invent, round creatively,
or recall figures from memory. If you need a number that is not in DATA, write [NEED: description] instead.
"""
    sel = [data["headlines"][i] for i in plan.get("selected_headline_ids", []) if i < len(data["headlines"])]
    facts = [f for f in data["facts"] if f["company"] in plan.get("facts_to_use", [])] or data["facts"]
    recent = [{"title": p["title"], "snippet": p["snippet"], "date": p["publishDate"]} for p in recent_posts]

    user = f"""ANGLE: {plan['angle']}
WORKING TITLE: {plan['working_title']}
WHY NOW: {plan.get('why_now', '')}

DATA (the only permitted source of numbers):
{json.dumps(facts, ensure_ascii=False, indent=1)}

SUPPORTING HEADLINES (context only, quote numbers from them sparingly and only if they also appear here verbatim):
{json.dumps(sel, ensure_ascii=False, indent=1)}

RECENT ARTICLES (do not repeat these theses):
{json.dumps(recent, ensure_ascii=False, indent=1)}

Write an 800-1100 word article in English. Use 2-4 short H2 headings (##), no H1. Open with the sharpest fact,
not a scene-setter. Link once to a relevant recent article using its slug if one fits: /blog/<slug>.
End on a forward-looking judgement, not a summary.

Return ONLY JSON:
{{
  "title": "<= 70 chars, contains a searchable keyword",
  "snippet": "<= 160 chars, one sentence",
  "slug": "kebab-case-slug",
  "tags": ["3-5 tags"],
  "category": "Market" | "Policy" | "Supply Chain" | "Brands" | "Opinion",
  "body_markdown": "..."
}}"""
    return system, user
