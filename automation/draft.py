"""Layers 2+3 - Select + Write + Validate.

Reads automation/data/<week>.json, makes two Claude calls, writes
src/content/blog/<slug>.md with draft: true, plus automation/out/<week>.review.md
(reviewer note: thesis, editor questions, unverified numbers).

Usage:
    python automation/draft.py                 # current week
    python automation/draft.py --week 2026-W39
    python automation/draft.py --dry-run       # build prompts only, no API call

Env: ANTHROPIC_API_KEY, optional ANTHROPIC_MODEL (default claude-sonnet-4-5)
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from pathlib import Path

import yaml

import prompts
import validate
from common import BLOG_DIR, DATA_DIR, ROOT, iso_week_label, log

OUT_DIR = ROOT / "out"
DEFAULT_MODEL = os.environ.get("ANTHROPIC_MODEL", "claude-sonnet-4-5")
UNSPLASH_POOL = [
    "photo-1593941707882-a5bba14938c7", "photo-1566367576585-051277d52997",
    "photo-1492144534655-ae79c964c9d7", "photo-1494412519320-aa613dfb7738",
    "photo-1560958089-b8a1929cea89", "photo-1554744512-d6c603f27c54",
]


def recent_posts(n: int = 6) -> list[dict]:
    posts = []
    for p in BLOG_DIR.glob("*.md"):
        text = p.read_text(encoding="utf-8", errors="ignore")
        m = re.match(r"^---\n(.*?)\n---", text, re.S)
        if not m:
            continue
        try:
            fm = yaml.safe_load(m.group(1)) or {}
        except yaml.YAMLError:
            continue
        posts.append({"slug": p.stem, "title": fm.get("title", ""), "snippet": fm.get("snippet", ""),
                      "publishDate": str(fm.get("publishDate", ""))})
    posts.sort(key=lambda x: x["publishDate"], reverse=True)
    return posts[:n]


def call_claude(system: str | None, user: str, max_tokens: int) -> str:
    import anthropic  # local import so --dry-run works without the key

    client = anthropic.Anthropic()
    kwargs = {"model": DEFAULT_MODEL, "max_tokens": max_tokens,
              "messages": [{"role": "user", "content": user}]}
    if system:
        kwargs["system"] = system
    msg = client.messages.create(**kwargs)
    return "".join(getattr(b, "text", "") for b in msg.content)


def parse_json(raw: str) -> dict:
    raw = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw.strip(), flags=re.S)
    return json.loads(raw[raw.find("{"): raw.rfind("}") + 1])


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", s.lower()).strip("-")[:80] or "weekly-brief"


def build_markdown(article: dict, week: str) -> str:
    fm = {
        "draft": True,
        "title": article["title"],
        "snippet": article["snippet"],
        "image": UNSPLASH_POOL[sum(map(ord, week)) % len(UNSPLASH_POOL)],
        "publishDate": dt.date.today().isoformat(),
        "category": article.get("category", "Market"),
        "author": "AutoChina Research",
        "tags": article.get("tags", []),
    }
    fm_text = yaml.safe_dump(fm, allow_unicode=True, sort_keys=False, default_flow_style=None).strip()
    return f"---\n{fm_text}\n---\n\n{article['body_markdown'].strip()}\n"



def review_note(week: str, plan: dict, article: dict, flagged: list[str], data: dict, path: Path) -> str:
    lines = [
        f"# Review: {week}", "",
        f"**File:** `{path.relative_to(ROOT.parent).as_posix()}`",
        f"**Title:** {article['title']}",
        f"**Thesis:** {plan['angle']}",
        f"**Why now:** {plan.get('why_now', '')}",
        "", "## Numbers that could NOT be verified against data JSON",
    ]
    lines += [f"- [ ] `{t}`" for t in flagged] if flagged else ["- none ✅"]
    needs = re.findall(r"\[NEED:[^\]]*\]", article["body_markdown"])
    if needs:
        lines += ["", "## Gaps the model asked you to fill"] + [f"- [ ] {n}" for n in needs]
    lines += ["", "## Editor questions"] + [f"- [ ] {q}" for q in plan.get("editor_questions", [])]
    if data.get("failures"):
        lines += ["", "## Sources that failed this week"] + [f"- {f}" for f in data["failures"]]
    lines += ["", "## Sources used"] + [f"- {f['company']}: {f['url']}" for f in data["facts"]]
    lines += ["", "To publish: set `draft: false`, adjust `publishDate`, merge."]
    return "\n".join(lines) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", default=iso_week_label())
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    data_path = DATA_DIR / f"{args.week}.json"
    if not data_path.exists():
        log(f"no data file {data_path}; run collect.py first")
        return 2
    data = json.loads(data_path.read_text(encoding="utf-8"))
    if not data["headlines"] and not data["facts"]:
        log("nothing collected this week; skipping draft")
        return 3

    OUT_DIR.mkdir(exist_ok=True)
    sel_prompt = prompts.select_prompt(data)
    if args.dry_run:
        (OUT_DIR / f"{args.week}.select_prompt.txt").write_text(sel_prompt, encoding="utf-8")
        fake_plan = {"angle": "dry run", "working_title": "dry", "selected_headline_ids": [0, 1, 2],
                     "facts_to_use": [f["company"] for f in data["facts"]], "why_now": "", "editor_questions": []}
        system, user = prompts.write_prompt(data, fake_plan, recent_posts())
        (OUT_DIR / f"{args.week}.write_prompt.txt").write_text(system + "\n\n=====\n\n" + user, encoding="utf-8")
        log(f"dry run: prompts in {OUT_DIR} (select={len(sel_prompt)} chars, write={len(system) + len(user)} chars)")
        return 0

    log("LLM call 1/2: select angle")
    plan = parse_json(call_claude(None, sel_prompt, 1500))
    log(f"  angle: {plan['angle']}")

    log("LLM call 2/2: write draft")
    system, user = prompts.write_prompt(data, plan, recent_posts())
    article = parse_json(call_claude(system, user, 6000))

    flagged = validate.check(article["body_markdown"], data)
    slug = slugify(article.get("slug") or article["title"])
    md_path = BLOG_DIR / f"{slug}.md"
    md_path.write_text(build_markdown(article, args.week), encoding="utf-8")

    (OUT_DIR / f"{args.week}.review.md").write_text(review_note(args.week, plan, article, flagged, data, md_path), encoding="utf-8")
    (OUT_DIR / f"{args.week}.plan.json").write_text(json.dumps(plan, ensure_ascii=False, indent=2), encoding="utf-8")

    if gh := os.environ.get("GITHUB_OUTPUT"):  # expose to the workflow
        with open(gh, "a", encoding="utf-8") as fh:
            fh.write(f"slug={slug}\ntitle={article['title']}\nflagged={len(flagged)}\n")

    log(f"wrote {md_path}\nunverified numbers: {flagged or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
