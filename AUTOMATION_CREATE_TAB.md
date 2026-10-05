# Cursor Automation — Exact Setup

## Automation type

Scheduled Automation

## Repository

Attach this private GitHub repository. The automation branch is `main`.

## Model

Preferred: a current high-capability thinking model.
Do not use a low-cost model for the end-to-end application run.

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

Before changing `RUN_MODE` to `LIVE`, complete the blank fields in `config/job_preferences.md`, `config/answer_bank.md`, and `config/target_config_block.md`, and set `SPREADSHEET_ID`.
