# AutoChina weekly draft pipeline

Every Monday 06:00 UTC a GitHub Action collects official numbers + a week of headlines,
asks Claude to pick one angle and write an 800–1100 word draft, validates every number in the
draft against the collected data, and opens a pull request. A human reads, edits, sets
`draft: false`, merges. Cloudflare Pages deploys on merge.

```
collect.py ──► data/YYYY-Www.json ──► draft.py ──► src/content/blog/<slug>.md (draft: true)
   │                                     │              out/YYYY-Www.review.md  (PR body)
   ├─ hkex.py   HKEX monthly volume PDFs  └─ validate.py  numbers ⊆ data ?
   └─ RSS / Google News RSS
```

## Source principle

Never scrape brand or government home pages (JS shells, anti-bot). Only pull from outlets
designed for machines:

| Need | Source | Status |
|---|---|---|
| BYD / Geely / NIO / XPeng / Li monthly volume | HKEX `titleSearchServlet` → static PDF | ✅ tested |
| CPCA (乘联会) retail / wholesale | Google News RSS `乘联会 零售` (syndicated copies carry identical numbers) | ✅ tested |
| CAAM, MIIT, Xiaomi deliveries | Google News RSS keyword monitors | ✅ tested |
| English EV / trade coverage | cnevpost, carnewschina, electrek RSS | ✅ tested |
| US-listed OEM IR | GlobeNewswire / PR Newswire RSS with keyword filter | ⚠️ filter often yields 0 in a given week; marked "failed" not fatal |

A source that fails is listed under **Sources that failed this week** in the PR — the editor
fills the gap manually or ignores it.

## Number provenance

`validate.py` extracts every numeric token from the draft and checks it against
`facts` (official PDFs) and `headlines`, including k / 万 / million scalings and sign-stripped
values (`-6.84` → "down 6.84%"). Percentages must match **official facts only**.
Anything unmatched becomes a checkbox in the PR and the PR gets label `needs-fact-check`.
The model is also instructed to write `[NEED: …]` instead of guessing.

## Run locally

```powershell
pip install -r automation/requirements.txt
cd automation
python collect.py                 # -> data/2026-W39.json
python draft.py --dry-run         # writes both prompts to out/ without calling the API
$env:ANTHROPIC_API_KEY = "sk-ant-..."
python draft.py                   # -> ../src/content/blog/<slug>.md + out/<week>.review.md
python validate.py ../src/content/blog/<slug>.md data/2026-W39.json
```

## GitHub setup (one-time)

1. Repo **Settings → Secrets and variables → Actions → New repository secret**
   `ANTHROPIC_API_KEY`.
2. Optional variable `ANTHROPIC_MODEL` (defaults to `claude-sonnet-4-5`).
3. **Settings → Actions → General → Workflow permissions**: "Read and write" +
   "Allow GitHub Actions to create and approve pull requests".
4. Trigger once manually: **Actions → Weekly AutoChina draft → Run workflow**.

## Editor's weekly routine (~20 min)

1. Open the PR. Read the body: thesis, editor questions, unverified numbers, failed sources.
2. Tick each unverified number (fix or delete it in the markdown).
3. Change 1–2 judgement sentences; add one line that is unmistakably yours.
4. Set `draft: false`, fix `publishDate`, merge. Or close the PR to skip the week.

## Tuning

- Sources: `sources.yml` (add a Google News query or RSS feed; no code change).
- Voice: `.writtingrules` at repo root is read as the system prompt when present locally.
  It is git-ignored, so CI uses the compact fallback in `prompts.py`. Copy the rules into
  `prompts._FALLBACK_STYLE` if you want CI to use the full version.
- Editorial criteria: `prompts.select_prompt`.

## Not yet wired (needs accounts)

Distribution after merge — X/LinkedIn slices via Buffer or Typefully, newsletter via
Beehiiv — is a separate `on: push` workflow to add once those API keys exist.
