"""HKEX disclosure collector.

Every HK-listed OEM files monthly production/sales volume as a static PDF.
We hit the same JSON servlet the HKEXnews search page uses, then parse the PDF.
"""
from __future__ import annotations

import datetime as dt
import io
import json
import re

from pypdf import PdfReader

from common import get, log, num

MONTHS = "January|February|March|April|May|June|July|August|September|October|November|December"
BASE = "https://www1.hkexnews.hk"


def stock_id(code: str) -> int | None:
    r = get(f"{BASE}/search/prefix.do",
            params={"callback": "cb", "lang": "EN", "type": "A", "name": code, "market": "SEHK"})
    m = re.search(r'"stockId":\s*"?(\d+)', r.text) if r else None
    return int(m.group(1)) if m else None


def titles(sid: int, since: dt.date) -> list[dict]:
    r = get(f"{BASE}/search/titleSearchServlet.do", params={
        "sortDir": 0, "sortByOptions": "DateTime", "category": 0, "market": "SEHK",
        "stockId": sid, "documentType": -1,
        "fromDate": since.strftime("%Y%m%d"), "toDate": dt.date.today().strftime("%Y%m%d"),
        "title": "", "searchType": 1, "t1code": -2, "t2Gcode": -2, "t2code": -2,
        "rowRange": 100, "lang": "EN",
    })
    if not r:
        return []
    rows = r.json().get("result")
    return json.loads(rows) if isinstance(rows, str) else (rows or [])


def pdf_text(url: str) -> str:
    r = get(url, timeout=40)
    if not r:
        return ""
    try:
        return "\n".join((p.extract_text() or "") for p in PdfReader(io.BytesIO(r.content)).pages)
    except Exception as e:  # noqa: BLE001
        log(f"  pdf parse failed: {e}")
        return ""


def parse_byd_table(text: str) -> dict:
    """BYD PDF rows carry 10 values: 4 production counts, prod YTD yoy%, 4 sales counts, sales YTD yoy%."""
    flat = re.sub(r"\s+", " ", text)
    m = re.search(rf"FOR ({MONTHS}) (\d{{4}})", flat, re.I)
    period = f"{m.group(1)} {m.group(2)}" if m else None
    row_re = re.compile(
        r"(New energy vehicle|Passenger vehicle|Battery electric vehicle|Plug-in hybrid electric vehicle|Commercial vehicle)"
        r"\s+((?:[\d,]+\s+){4}-?[\d.]+%\s+(?:[\d,]+\s+){4}-?[\d.]+%)", re.I)
    segments = {}
    for name, nums in row_re.findall(flat):
        p = nums.split()
        if len(p) != 10:
            continue
        seg = {
            "production": num(p[0]), "production_ly": num(p[1]),
            "production_ytd": num(p[2]), "production_ytd_ly": num(p[3]),
            "production_ytd_yoy_pct": float(p[4].rstrip("%")),
            "sales": num(p[5]), "sales_ly": num(p[6]),
            "sales_ytd": num(p[7]), "sales_ytd_ly": num(p[8]),
            "sales_ytd_yoy_pct": float(p[9].rstrip("%")),
        }
        if seg["sales_ly"]:
            seg["sales_month_yoy_pct"] = round((seg["sales"] / seg["sales_ly"] - 1) * 100, 2)
        segments[name.lower()] = seg
    m2 = re.search(r"overseas[^\d%]{0,120}?([\d,]{5,})", flat, re.I)
    if m2:
        segments["overseas"] = {"sales": num(m2.group(1))}
    return {"period": period, "segments": segments}


def parse_generic(text: str) -> dict:
    """Fallback for NIO/XPeng/Li/Geely: harvest every large integer near a delivery/sales verb."""
    flat = re.sub(r"\s+", " ", text)
    m = re.search(rf"({MONTHS}) (\d{{4}})", flat)
    period = f"{m.group(1)} {m.group(2)}" if m else None
    figures, seen = [], set()
    for m in re.finditer(r"\b(\d{1,3}(?:,\d{3})+|\d{4,})\b", flat):
        value = num(m.group(1))
        if 1900 <= value <= 2100 or value in seen:      # skip years and duplicates
            continue
        ctx = flat[max(0, m.start() - 140): m.end() + 60].strip()
        if not re.search(r"deliver|sold|sales|volume|unit|vehicle|cumulative|total", ctx, re.I):
            continue
        seen.add(value)
        figures.append({"value": value, "context": ctx})
    return {"period": period, "figures": figures, "excerpt": flat[:1500]}


def collect(cfg: list[dict], since: dt.date) -> tuple[list[dict], list[str]]:
    facts, failures = [], []
    for item in cfg:
        log(f"[hkex] {item['name']}")
        sid = stock_id(item["code"])
        if not sid:
            failures.append(f"hkex:{item['name']}: stockId lookup failed")
            continue
        rows = [r for r in titles(sid, since) if re.search(item["title_regex"], r.get("TITLE", ""), re.I)]
        if not rows:
            log("  no matching announcement in window")
            continue
        row = rows[0]
        url = BASE + row["FILE_LINK"]
        text = pdf_text(url)
        if not text:
            failures.append(f"hkex:{item['name']}: pdf unreadable {url}")
            continue
        parsed = parse_byd_table(text) if item["parser"] == "byd_table" else parse_generic(text)
        facts.append({"company": item["name"], "source": "HKEX", "title": row["TITLE"].strip(),
                      "published": row["DATE_TIME"], "url": url, **parsed})
    return facts, failures
