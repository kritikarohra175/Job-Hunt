# Job Hunt

Control repository for an entry-level digital marketing, social media, content, and SEO job-application workflow.

The only authoritative resume is `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`. Older resume files are not used.

## Runtime

`config/runtime.md` sets:

```
RUN_MODE=LIVE
MAX_APPLICATIONS_PER_RUN=1
MAX_APPLICATIONS_PER_DAY=10
AUTO_APPLY_THRESHOLD=85
```

`REVIEW_ONLY` never submits an application and never clicks a final Submit or Apply button. `LIVE` may submit only when every application rule and hard stop is satisfied.

LinkedIn and Naukri are not submitted by the run when the listing cannot be fully accessed or safely automated. An eligible listing is recorded as `Manual Apply` with its URL, score, deadline, salary, and hold reason.

## Tracker

Google Sheets is the application-history authority. `data/application_tracker.csv` is a backup cache. Deduplication checks both, and a GitHub commit of the CSV is not enough.

The spreadsheet ID, tab, and Drive resume file ID are in `config/runtime.md`.

## Checks

```
.venv/bin/python scripts/validate_config.py
```

PDF dependencies are listed in `requirements.txt` and installed by `.cursor/environment.json`.

Do not commit passwords, tokens, cookies, API keys, or session files.
