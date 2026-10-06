# Cursor Automation

One automation is already connected to this repository: Job Hunt (`bee28e3c-c04e-11f1-bb68-864e54d14197`).

Use repository `kritikarohra175/Job-Hunt` and branch `main`. Do not point the recurring run at a `cursor/...` feature branch.

The instructions must be the current contents of `prompts/daily_automation_prompt.md`.

Keep `config/runtime.md` at `RUN_MODE=REVIEW_ONLY` for review tests. That mode never submits an application.

Schedule, when the automation is turned on: weekdays at 09:00 and 17:00 `Asia/Kolkata`.

```
0 9,17 * * 1-5
```

Connect GitHub, Google Drive, Google Sheets, and Gmail. Use Cursor's browser tools. Do not add a second browser connector.

Google Sheets is the application-history authority. `data/application_tracker.csv` is only a cache.
