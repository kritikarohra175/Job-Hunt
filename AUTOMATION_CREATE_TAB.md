# Cursor Automation — Exact Setup

## Automation type

Scheduled Automation

## Repository

Attach this private GitHub repository. The automation branch is `main`.

## Model

Use Claude Sonnet 4.6 for the current known-good test, or Auto if Cursor should choose the model. Do not switch models while debugging the workflow unless necessary.

## Computer Use

Enabled.

## MCPs / Plugins

Enable:

- GitHub
- Google Drive
- Gmail
- Google Sheets

Google Sheets is the application-history authority. The CSV in git is only a cache.

Use Cursor native Browser / Computer Use. Do not add multiple browser MCPs initially.

## Schedule

Recommended first schedule: weekdays at 09:00 and 17:00 IST.

Cron:

`0 9,17 * * 1-5`

If Cursor requires an explicit timezone field, use `Asia/Kolkata`.

## Automation prompt

Copy the prompt from `prompts/daily_automation_prompt.md` into the automation instructions.

## Mode

Keep `RUN_MODE=REVIEW_ONLY` in `config/runtime.md` for the first runs. That mode must not submit applications.

Before changing `RUN_MODE` to `LIVE`, set `SPREADSHEET_ID` in `config/runtime.md` to the real Google Sheet ID. Do not invent it. Approved preference and answer fields are already filled.
