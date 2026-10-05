# Cursor MCP / Connector Setup

## Required

### 1. GitHub

Status: already connected by the user.
Purpose:
- private repository source control
- automation repository access
- versioning of instructions/configuration

Do not store job-board passwords or Google OAuth secrets in GitHub.

### 2. Google Drive

Install the official Cursor Google Drive plugin.
Purpose:
- store master resume
- store tailored resumes
- store cover letters
- store application evidence

Keep the master resume in a dedicated folder such as:
`Job Applications/Master Resume/`

### 3. Gmail

Install the official Cursor Gmail plugin.
Purpose:
- read application confirmations
- detect recruiter responses
- optionally draft follow-ups

Do not auto-send recruiter emails unless separately enabled.

### 4. Google Sheets

Install the official Google Sheets plugin if available in Customize / Marketplace.
Purpose:
- maintain the application tracker
- append one row per opportunity
- update application status
- record resume version and evidence

If Google Sheets is not available in the user's Cursor workspace, use a trusted Google Workspace-capable alternative such as Composio rather than hard-coding credentials.

## Browser / Computer Use

Use Cursor's native Browser / Computer Use. Do NOT install three overlapping browser MCPs at the start.

Playwright can be added later as a fallback for specific browser workflows, not as the primary stack.

## Not required initially

- Slack
- Notion
- Hunter
- generic scraping MCPs
- multiple browser-control MCPs

## Principle

Use the fewest trusted connectors necessary. Cursor Automations already support computer use and can connect MCP servers. Official plugins are preferred over unreviewed community servers.
