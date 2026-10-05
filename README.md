# Job Hunt

Control repository for an entry-level digital marketing, social media, content, and SEO job-application workflow.

The only authoritative resume is `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`. Older resume files are not used.

## Runtime

`config/runtime.md` sets:

```
RUN_MODE=REVIEW_ONLY
MAX_APPLICATIONS_PER_RUN=5
MAX_APPLICATIONS_PER_DAY=10
AUTO_APPLY_THRESHOLD=85
```

`REVIEW_ONLY` never submits an application and never clicks a final Submit or Apply button. Run two review-only tests before changing the mode. `LIVE` may submit only when every application rule and hard stop is satisfied and the missing user fields are filled.

## Tracker

Google Sheets is the application-history authority. `data/application_tracker.csv` is a backup cache. Deduplication does not depend on a GitHub commit.

The spreadsheet ID is still `NOT_CONFIGURED`.

## Checks

```
python3 scripts/validate_config.py
```

PDF dependencies are listed in `requirements.txt` and installed by `.cursor/environment.json`.

Do not commit passwords, tokens, cookies, API keys, or session files.
