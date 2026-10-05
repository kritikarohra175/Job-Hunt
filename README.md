# Cursor Job Application Agent — Fixed Configuration

This repository is the control plane for a scheduled job-search and application workflow.

## Authoritative state
- GitHub: rules and configuration only.
- Google Drive: master resume + tailored PDF archive.
- Google Sheets: authoritative application history.
- Gmail: confirmations/interview evidence.

## Before LIVE mode
1. Keep `config/runtime.md` at `RUN_MODE=REVIEW_ONLY`.
2. Fill every TODO in `config/job_preferences.md`.
3. Fill salary/work authorization/visa/relocation answers in `config/answer_bank.md`.
4. Put the final resume in Google Drive: `Job Applications/Master Resume/`.
5. Ensure Google Sheets contains `Job Applications — Master Tracker`.
6. Create a Cursor Cloud Environment so `reportlab` and `pypdf` are installed.
7. Run two REVIEW_ONLY tests.
8. Only after those pass, change `RUN_MODE=LIVE`.

## Resume generation
Tailored application files must be real PDFs generated through `scripts/build_resume_pdf.py`. Markdown is never an application attachment.
