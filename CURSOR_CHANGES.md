# Cursor changes after replacing the repo contents

## Automation repository
Select repository `kritikarohra175/Job-Hunt` and branch `main`.

The recording showed a stale generated branch error involving:
`cursor/digital-marketing-resume-automation-b93f`

Do not use that generated branch as the recurring automation branch. Cursor's scheduled automations use the repository and branch selected in the automation settings.

## Automation prompt
Paste the complete contents of `prompts/daily_automation_prompt.md`.

## Model
Use Claude Sonnet 4.6 for the current known-good test, or Auto if you prefer model selection to be managed by Cursor. Do not change models while debugging the workflow unless necessary.

## Tools
Enable:
- GitHub
- Google Drive
- Google Sheets
- Gmail
- Cursor native Browser / Computer Use

Do not add multiple browser MCPs yet.

## Runtime
Keep `config/runtime.md` at `RUN_MODE=REVIEW_ONLY` for the next two tests.
Only after the two tests pass should you change it to `RUN_MODE=LIVE`.

## Environment
Create/enable the Cloud Environment for this repository so the included `.cursor/environment.json` installs `reportlab` and `pypdf`.

## Data stores
- Google Drive = master resume and tailored PDFs.
- Google Sheets = authoritative application history.
- GitHub = configuration/control plane.
- `data/application_tracker.csv` = backup/cache, not the authoritative source.

## Critical resume rule
Never attach `.md`, `.txt`, or a draft file to an application. The agent must create and validate a real PDF using `scripts/build_resume_pdf.py` before submitting.
