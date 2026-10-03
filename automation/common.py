"""Shared helpers for the AutoChina automation pipeline."""
from __future__ import annotations

import datetime as dt
import sys
import time
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parent
DATA_DIR = ROOT / "data"
BLOG_DIR = REPO / "src" / "content" / "blog"
UA = "Mozilla/5.0 (compatible; AutoChinaBot/0.1; +https://autochina.org)"

SESSION = requests.Session()
SESSION.headers["User-Agent"] = UA


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def get(url: str, timeout: int = 20, **kw) -> requests.Response | None:
    """GET with 3 retries. Returns None instead of raising so one dead source never kills the run."""
    for attempt in range(3):
        try:
            r = SESSION.get(url, timeout=timeout, **kw)
            if r.status_code == 200:
                return r
            log(f"  http {r.status_code} {url}")
        except requests.RequestException as e:
            log(f"  {type(e).__name__} {url}")
        time.sleep(2 * (attempt + 1))
    return None


def iso_week_label(d: dt.date | None = None) -> str:
    d = d or dt.date.today()
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def num(s: str) -> int:
    return int(s.replace(",", ""))
