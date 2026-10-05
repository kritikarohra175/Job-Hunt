# START HERE

## 1. Create a private GitHub repository

Recommended name:
`cursor-job-application-agent`

Keep it private.

## 2. Copy this folder into the repo

The repository should contain:
- `AGENTS.md`
- `.cursor/rules/job-application-agent.mdc`
- `config/`
- `data/`
- `templates/`
- `prompts/`

## 3. Connect Cursor integrations

Already connected:
- GitHub

Connect in Cursor Customize:
- Google Drive
- Gmail
- Google Sheets (or a trusted Google Workspace-capable alternative if Sheets is unavailable)

Use Cursor's native Browser / Computer Use.

## 4. Put the source resume in Google Drive

Create:
`Job Applications/Master Resume/`

Upload the final source resume there.

## 5. Complete configuration

Edit `config/job_preferences.md` and replace every `TODO` with an explicit value.

Edit `config/answer_bank.md` and replace the required `NOT CONFIGURED` fields with exact approved answers.

Do not let the agent guess these fields.

## 6. Create the tracker

Import `data/application_tracker.csv` into a Google Sheet named:
`Job Applications — Master Tracker`

## 7. Create the Cursor Automation

Use `AUTOMATION_CREATE_TAB.md`.

Recommended schedule:
`0 9,17 * * 1-5`
Timezone: `Asia/Kolkata`
Model: `Claude Sonnet 5.5` (Thinking if available), fallback `Auto`.

Paste `prompts/daily_automation_prompt.md` as the automation instructions.

Attach this repository.

## 8. First phase: review mode

Run the first several scheduled runs without autonomous submission. Verify:
- correct job filtering
- correct duplicate detection
- correct resume tailoring
- correct application answers
- correct tracker updates

Then enable autonomous submission only for the explicit, permitted routine flows defined by the rules.
