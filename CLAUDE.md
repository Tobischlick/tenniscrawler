# CLAUDE.md

Guidance for Claude Code when working in this repository.

## What this is

**TennisCrawler** is a Python scraper for the Badischer Tennisverband (nuliga)
website. It walks regional "Bezirk" pages down through leagues → teams →
clubs → club sites to collect contact emails, and exports the results as CSV
into `Excelfiles/`. No framework — just `requests` + `bs4`.

## Structure

- [crawler.py](crawler.py) — entrypoint. Reads `.config/config.ini`, then runs
  the pipeline stage by stage: `CrawledGroups` → `CrawledTeams` →
  `CrawledClubs` → `CrawledMails`, deduplicating club sites in between.
- [src/crawler/](src/crawler/) — one class per pipeline stage
  (`crawled_groups.py`, `crawled_teams.py`, `crawled_clubs.py`,
  `crawled_mails.py`), each with a `fetch()` that writes its stage's CSV to
  `Excelfiles/`.
- [src/helper/](src/helper/) — `terminal.py` (console/log output),
  `delete_duplicates.py` (dedupes club sites between stages).
- [.config/config.ini](.config/config.ini) — `[URLS]` (Bezirk pages to crawl)
  and `[MAILS]` (keyword filters for which addresses to keep). Keys are
  arbitrary; only values are read.
- `Excelfiles/` — pipeline output (`01_...csv` through `04_Mails.csv`).
- `Logfiles/` — run logs.
- [.github/workflows/linter.yml](.github/workflows/linter.yml) — Pylint over
  `git ls-files '*.py'`, `--fail-under=8.0`.
- [.github/workflows/osv-scanner-pr.yml](.github/workflows/osv-scanner-pr.yml) /
  [osv-scanner.yml](.github/workflows/osv-scanner.yml) — OSV-Scanner on PRs to
  `main` (fails only on newly introduced vulns) and daily/on push to `main`
  (SARIF → Security tab). Ignores go in [osv-scanner.toml](osv-scanner.toml)
  with `reason` and `ignoreUntil`.
- `requirements.in` / `requirements-dev.in` — direct deps. `requirements.txt` /
  `requirements-dev.txt` are pip-compile lock files (all transitive deps
  pinned); never edit them by hand. Renovate updates them via its
  `pip-compile` manager.
- [.pylintrc](.pylintrc) — max line length 127; docstring/too-few-public-methods
  checks disabled (stage classes are intentionally thin).

## Running things locally

```bash
source venv/bin/activate && python crawler.py
```

```bash
pylint $(git ls-files '*.py') --fail-under=8.0
```

After changing a `.in` file, regenerate the lock files (needs `pip-tools`):

```bash
pip-compile --strip-extras --output-file=requirements.txt requirements.in
pip-compile --strip-extras --output-file=requirements-dev.txt requirements-dev.in
```

## Before starting any task

Always pull the latest `main` before doing anything in this repo (creating a
branch, editing files, etc.):

```bash
git checkout main && git pull
```

## Branching & commit conventions

**Branches**

- If a GitHub issue exists: `feature/ISSUE-XX-short-description` (e.g.
  `feature/ISSUE-28-add-claude-md`).
- If there is no issue: `feature/NO-ISSUE-short-description`.

**Commits**

- Clean, short one-liners. No multi-paragraph bodies, no bullet-point
  changelogs in the commit message.
