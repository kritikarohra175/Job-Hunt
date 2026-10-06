# Cursor Automation

One automation is already connected to this repository: Job Hunt (`bee28e3c-c04e-11f1-bb68-864e54d14197`).

Use repository `kritikarohra175/Job-Hunt` and branch `main`. Do not point the recurring run at a `cursor/...` feature branch.

The instructions must be the current contents of `prompts/daily_automation_prompt.md`.

`config/runtime.md` is `RUN_MODE=LIVE` with `MAX_APPLICATIONS_PER_RUN=1`. Submit only when every application rule and hard stop is satisfied.

Schedule, when the automation is turned on: weekdays at 09:00 and 17:00 `Asia/Kolkata`.

```
0 9,17 * * 1-5
```

Connect GitHub, Google Drive, Google Sheets, and Gmail. Use Cursor's browser tools. Do not add a second browser connector.

Google Sheets is the application-history authority. `data/application_tracker.csv` is only a cache.
