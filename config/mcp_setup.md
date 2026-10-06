# Cursor MCP / Connector Setup

## Required

### 1. GitHub

Status: already connected by the user.
Purpose:

- private repository source control
- automation repository access
- versioning of instructions and configuration

Do not store job-board passwords, Google OAuth secrets, API keys, cookies, or session tokens in GitHub.

The GitHub CSV at `data/application_tracker.csv` is a backup cache. It is not the application-history authority.

### 2. Google Drive

Install the official Cursor Google Drive plugin.
Purpose:

- store copies of tailored resume PDFs
- store cover letters
- store application evidence

The authoritative resume file inside this repository is `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`.
Do not replace it with an older resume from Drive.
Do not overwrite that file from an automation run.

Drive folders and the only usable Drive resume:

- Master Resume folder: `1cfBsRht8TOJ7e5PsBcIRlnoQrUdUaOG8`
- Tailored Resumes folder: `1uoZnYXfHaCa8jRC9aEQ3BLq3NFFwq_Fo`
- DRIVE_MASTER_RESUME_FILE_ID=1xjtepznMiLTdQnWGMIujIlWww15PY5UX

That Drive file is named `Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf` and is a byte-identical copy of `reference/Karina_Rohra_Digital_Marketing_Resume_FINAL.pdf`. If Drive and this repository disagree, stop. Do not merge resume versions. Do not open any other resume PDF on Drive, including older files whose names contain "final".

### 3. Gmail

Install the official Cursor Gmail plugin.
Purpose:

- read application confirmations
- detect recruiter responses
- optionally draft follow-ups

Do not auto-send recruiter emails unless separately enabled in configuration. Recruiter outreach is disabled.

### 4. Google Sheets

Google Sheets is the authoritative application-history tracker.

Spreadsheet name: `Job Applications — Master Tracker`
Tab: `Applications`
SPREADSHEET_ID=1M-cW2cUDfcUAQTGU5T9pNMs_rW_pXZhvhq-kjasD6JI

The ID is also recorded in `config/runtime.md`. It was read from the connected Google account. Do not invent a different ID.

Use the official Google Sheets plugin. Do not hard-code credentials.
Append or update one row per opportunity.
Deduplicate against this Sheet. Do not treat a GitHub commit of the CSV as application history.

If the Sheet is not configured or cannot be read, mark deduplication incomplete and do not submit.

## Browser / Computer Use

Use Cursor's native Browser / Computer Use. Do not install overlapping browser MCPs at the start.

Playwright can be added later as a fallback for a specific permitted browser workflow, not as the primary stack.

## Not required initially

- Slack
- Notion
- Hunter
- generic scraping MCPs
- multiple browser-control MCPs

## Principle

Use the fewest trusted connectors necessary. Official plugins are preferred over unreviewed community servers.
Do not bypass a site that disallows automation.
