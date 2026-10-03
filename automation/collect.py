"""Layer 1 - Collector.

(a) official monthly volume disclosures from HKEX  -> structured numbers ("facts")
(b) one week of headlines from RSS / Google News RSS -> candidate topics

Output: automation/data/YYYY-Www.json
The LLM may never alter anything under "facts"; draft.py validates every
number in the generated article against this file.

Usage:
    python automation/collect.py                # current ISO week
    python automation/collect.py --week 2026-W39
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.parse
from pathlib import Path

import feedparser
import yaml

import hkex
from common import DATA_DIR, ROOT, get, iso_week_label, log


def gnews_url(query: str, lang: str) -> str:
    q = urllib.parse.quote(query)
    if lang == "zh":
        return f"https://news.google.com/rss/search?q={q}&hl=zh-CN&gl=CN&ceid=CN:zh-Hans"
    return f"https://news.google.com/rss/search?q={q}&hl=en-US&gl=US&ceid=US:en"


def entry_date(e) -> dt.datetime | None:
    t = e.get("published_parsed") or e.get("updated_parsed")
    return dt.datetime(*t[:6], tzinfo=dt.timezone.utc) if t else None


def strip_html(s: str) -> str:
    return re.sub(r"<[^>]+>", "", s or "").strip()


def collect_feed(feed_id: str, url: str, since: dt.datetime, limit: int, include: str | None) -> list[dict]:
    r = get(url)
    if not r:
        return []
    d = feedparser.parse(r.content)
    out = []
    for e in d.entries:
        when = entry_date(e)
        if when and when < since:
            continue
        title = strip_html(e.get("title", ""))
        summary = strip_html(e.get("summary", ""))[:400]
        if include and not re.search(include, f"{title} {summary}"):
            continue
        out.append({
            "source": feed_id,
            "outlet": (e.get("source") or {}).get("title") or d.feed.get("title", feed_id),
            "title": title,
            "link": e.get("link"),
            "published": when.isoformat() if when else None,
            "summary": summary,
        })
        if len(out) >= limit:
            break
    return out


def collect_headlines(cfg: dict, since: dt.datetime) -> tuple[list[dict], list[str]]:
    items, failures = [], []
    limit = cfg.get("max_headlines_per_source", 12)
    for g in cfg.get("google_news", []):
        log(f"[gnews] {g['id']}")
        got = collect_feed(g["id"], gnews_url(g["query"], g.get("lang", "en")), since, limit, None)
        items.extend(got) if got else failures.append(f"gnews:{g['id']}: empty")
    for f in cfg.get("rss", []):
        log(f"[rss] {f['id']}")
        got = collect_feed(f["id"], f["url"], since, limit, f.get("include_regex"))
        items.extend(got) if got else failures.append(f"rss:{f['id']}: empty")

    seen, uniq = set(), []
    for it in items:
        key = re.sub(r"\W+", "", it["title"].lower())[:60]
        if key not in seen:
            seen.add(key)
            uniq.append(it)
    return uniq, failures


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--week", help="ISO week label, e.g. 2026-W39 (default: today)")
    ap.add_argument("--config", default=str(ROOT / "sources.yml"))
    args = ap.parse_args()

    cfg = yaml.safe_load(Path(args.config).read_text(encoding="utf-8"))
    today = dt.date.today()
    week = args.week or iso_week_label(today)
    since_dt = dt.datetime.now(dt.timezone.utc) - dt.timedelta(days=cfg.get("window_days", 8))

    facts, f1 = hkex.collect(cfg.get("hkex", []), today - dt.timedelta(days=45))
    headlines, f2 = collect_headlines(cfg, since_dt)

    out = {
        "week": week,
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "window_days": cfg.get("window_days", 8),
        "facts": facts,
        "headlines": headlines,
        "failures": f1 + f2,
    }
    DATA_DIR.mkdir(exist_ok=True)
    path = DATA_DIR / f"{week}.json"
    path.write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    log(f"\nwrote {path}  facts={len(facts)} headlines={len(headlines)} failures={len(out['failures'])}")
    for f in out["failures"]:
        log(f"  ! {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
