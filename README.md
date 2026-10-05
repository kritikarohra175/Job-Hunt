# Cursor Job Application Agent

A private Cursor project for finding suitable entry-level digital marketing jobs, tailoring a truthful resume for each job, completing applications where permitted, and tracking every action.

## Intended use

This repository is the instruction/control layer. It is not the job-board login system and it does not contain API keys or OAuth secrets.

The agent must:

1. Find newly posted roles matching the candidate profile.
2. Deduplicate against prior applications.
3. Read the full job description before deciding.
4. Score the job against the rules.
5. Tailor the resume without inventing facts.
6. Generate and save a job-specific resume.
7. Apply only when the site/workflow permits automation and the application is routine.
8. Stop for CAPTCHAs, 2FA, legal/authorization questions, ambiguous factual questions, suspicious requests, or prohibited automation.
9. Record the outcome in the application tracker.

## Important

Keep this GitHub repository private. Do not commit API keys, cookies, browser profiles, passwords, OTPs, session tokens, or other secrets.

The candidate's source resume should be stored in Google Drive or another private document store and should be linked to from the automation. The current source resume is represented in `config/master_profile.md` so the agent has a structured factual reference.
