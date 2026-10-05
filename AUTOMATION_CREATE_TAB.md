# Cursor Automation — Exact Setup

## Automation type

Scheduled Automation

## Repository

Attach this private GitHub repository.

## Model

Preferred: Claude Sonnet 5.5 (Thinking if available).
Fallback: Auto.
Do not use a low-cost model for the end-to-end application run.

## Computer Use

Enabled.

## MCPs / Plugins

Enable:
- GitHub
- Google Drive
- Gmail
- Google Sheets (or a trusted Google Workspace-capable fallback if Sheets is unavailable)

Use Cursor native Browser / Computer Use. Do not add multiple browser MCPs initially.

## Schedule

Recommended first schedule: weekdays at 09:00 and 17:00 IST.

Cron:
`0 9,17 * * 1-5`

If Cursor requires an explicit timezone field, use `Asia/Kolkata`.

## Automation prompt

Copy the prompt from `prompts/daily_automation_prompt.md` into the automation instructions.

## Before enabling auto-submit

Complete these fields in `config/job_preferences.md`:
- target locations
- remote/hybrid/on-site preferences
- relocation
- countries/cities
- minimum salary
- shift preferences

Complete these fields in `config/answer_bank.md`:
- availability
- salary expectation
- work authorization
- visa sponsorship
- relocation

Run in dry/review mode for the first several runs and inspect the tracker before allowing autonomous submission.
