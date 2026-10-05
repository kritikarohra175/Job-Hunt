# START HERE

The repository layout is already in place. Do not recreate it from an older zip or from loose root files.

## Authoritative resume

`reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`

Do not replace it with an older resume.

## Mode

`config/runtime.md` is set to `RUN_MODE=REVIEW_ONLY`. Leave it there until a review-only run has been checked. Do not submit applications in that mode.

## Still required before LIVE submission

In `config/job_preferences.md` and `config/target_config_block.md`, the user still needs to set:

- target locations
- remote, hybrid, and on-site preferences
- relocation
- countries and cities
- minimum and preferred salary
- international salary rule
- shift preferences

In `config/answer_bank.md`, the user still needs exact answers for:

- salary expectation
- work authorization
- visa sponsorship
- relocation

Availability is already taken from the final resume: Immediately.

## Tracker

Create or connect a Google Sheet named `Job Applications — Master Tracker`, with a tab named `Applications`, and put its ID in `SPREADSHEET_ID` in `config/runtime.md`.

Until that ID is set, deduplication is incomplete and the workflow must not submit.

Import `data/application_tracker.csv` only as the header cache. The Sheet remains the authority.

## Automation

Use `AUTOMATION_CREATE_TAB.md`.
Paste `prompts/daily_automation_prompt.md` as the automation instructions.
Attach this repository on `main`.

Run `python3 scripts/validate_config.py` before the first automation test.
