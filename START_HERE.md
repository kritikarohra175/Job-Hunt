# START HERE

The repository layout is already in place. Do not flatten `config/`, `data/`, `prompts/`, `templates/`, `scripts/`, `reference/`, or `.cursor/`.

In Cursor Automation, select repository `kritikarohra175/Job-Hunt` and branch `main`. Do not use a stale `cursor/...` feature branch, including `cursor/digital-marketing-resume-automation-b93f`, as the recurring automation branch.

## Authoritative resume

`reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`

Do not replace it with an older resume.

## Mode

`config/runtime.md` is set to `RUN_MODE=REVIEW_ONLY`. Leave it there for the next two review-only tests. Do not submit applications in that mode. Change it to `LIVE` only after those tests and `SPREADSHEET_ID` is set to the real Google Sheet ID.

## Approved preferences

`config/job_preferences.md`, `config/answer_bank.md`, and `config/target_config_block.md` now contain the approved locations, work arrangements, relocation, salary rules, shifts, availability, work authorization, visa sponsorship, and salary answers.

Availability remains Immediately.

## Tracker

Create or connect a Google Sheet named `Job Applications — Master Tracker`, with a tab named `Applications`.

Paste its ID in `config/runtime.md` on the line `SPREADSHEET_ID=NOT_CONFIGURED`, replacing `NOT_CONFIGURED`. Mirror that value on `SPREADSHEET_ID=` in `config/target_config_block.md`. Do not invent an ID.

Until that ID is set, deduplication against Google Sheets is incomplete and the workflow must not submit. Still check `data/application_tracker.csv`. A match in either source is a duplicate.

Import `data/application_tracker.csv` only as the header cache. The Sheet remains the authority.

## Automation

Use `AUTOMATION_CREATE_TAB.md`.
Paste `prompts/daily_automation_prompt.md` as the automation instructions.
Attach this repository on `main`.

Run `python3 scripts/validate_config.py` before the first automation test.
